from flask import Flask, render_template, request, redirect, url_for  # Flask et ses fonctions utiles
import sqlite3  # Pour interagir avec la base de données SQLite
from datetime import datetime  # Pour récupérer la date et l'heure actuelles

# Création de l'application Flask
app = Flask(__name__)

# Route principale ("/") qui accepte les méthodes GET et POST
@app.route("/", methods=["GET", "POST"])
def index():
    result = None  # Dictionnaire des résultats d'une recherche utilisateur
    historique = []  # Historique global des recherches
    historique_utilisateur = []  # Historique des recherches d'un utilisateur spécifique
    vent_collectif = None  # Vent médian collectif du jour

    # Connexion à la base de données SQLite
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    # Ajoute la colonne 'prenom' dans la table historique_recherches si elle n'existe pas
    try:
        cursor.execute("ALTER TABLE historique_recherches ADD COLUMN prenom TEXT")
    except sqlite3.OperationalError:
        pass  # Ignore l'erreur si la colonne existe déjà

    # Récupération des vents du jour pour toutes les résidences, pour calculer le vent médian collectif
    cursor.execute("SELECT vent FROM meteo WHERE date = date('now')")
    vents = [row[0] for row in cursor.fetchall() if row[0] is not None]
    if vents:
        vents.sort()
        n = len(vents)
        # Calcul de la médiane
        vent_collectif = vents[n // 2] if n % 2 == 1 else (vents[n // 2 - 1] + vents[n // 2]) / 2

    # Si un formulaire a été soumis en POST (recherche d’un étudiant)
    if request.method == "POST":
        nom_recherche = request.form["nom"]  # Récupère le nom saisi
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Date et heure actuelles

        # Récupère les résidences associées à l'étudiant dont le nom est saisi
        cursor.execute("""   
            SELECT e.id, e.nom, e.prenom, r.ville, r.date_fin, r.id
            FROM etudiants e
            JOIN residences r ON e.id = r.etudiant_id
            WHERE e.nom = ?
        """, (nom_recherche.upper(),)) 
        rows = cursor.fetchall()

        if rows:
            # Première résidence trouvée
            id_, nom, prenom, ville1, _, res1_id = rows[0]
            ville2 = None  # Ville secondaire
            res2_id = None  # ID résidence secondaire

            # Recherche de la résidence secondaire (avec une date de fin non nulle)
            for row in rows[1:]:
                if row[4] is not None:
                    ville2 = row[3]
                    res2_id = row[5]

            # Récupère la vitesse du vent dans la résidence principale pour aujourd'hui
            cursor.execute("SELECT vent FROM meteo WHERE residence_id = ? AND date = date('now')", (res1_id,))
            vent1 = cursor.fetchone()
            vent1 = vent1[0] if vent1 else None

            # Récupère la vitesse du vent dans la résidence secondaire si elle existe
            vent2 = None
            if res2_id:
                cursor.execute("SELECT vent FROM meteo WHERE residence_id = ? AND date = date('now')", (res2_id,))
                res = cursor.fetchone()
                vent2 = res[0] if res else None

            # Insertion de la recherche dans l’historique
            cursor.execute("""
                INSERT INTO historique_recherches (nom, prenom, ville1, vent1, ville2, vent2, heure)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nom, prenom, ville1, vent1, ville2, vent2, now))

            # Stocke les résultats pour affichage
            result = {
                "nom": nom,
                "prenom": prenom,
                "ville1": ville1,
                "vent1": vent1,
                "ville2": ville2,
                "vent2": vent2
            }

    # Récupère les 10 dernières recherches globales
    cursor.execute("SELECT * FROM historique_recherches ORDER BY id DESC LIMIT 10")
    historique = cursor.fetchall()

    # Si une recherche a été effectuée, récupère tout l’historique de cet utilisateur
    if result:
        cursor.execute("SELECT * FROM historique_recherches WHERE nom = ?", (result["nom"],))
        historique_utilisateur = cursor.fetchall()

    # Sauvegarde les changements et ferme la connexion à la base de données
    conn.commit()
    conn.close()

    # Rend la page HTML avec les données à afficher
    return render_template("index.html", result=result, historique=historique,
                           historique_utilisateur=historique_utilisateur, vent_collectif=vent_collectif)

# Route pour effacer l’historique des recherches (via POST)
@app.route("/clear", methods=["POST"])
def clear_history():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    # Supprime uniquement les 10 dernières recherches globales (celles affichées à l’écran)
    cursor.execute("""
        DELETE FROM historique_recherches
        WHERE id IN (
            SELECT id FROM historique_recherches
            ORDER BY id DESC
            LIMIT 10
        )
    """)

    conn.commit()
    conn.close()
    return redirect(url_for("index"))


# Route pour afficher la liste des étudiants et leurs résidences
@app.route("/etudiants") # Route pour afficher la liste des étudiants et leurs résidences
def etudiants():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    # Récupère les informations des étudiants et de leurs résidences
    cursor.execute("""
        SELECT e.id, e.nom, e.prenom, e.groupe, r.ville, r.date_fin
        FROM etudiants e
        JOIN residences r ON e.id = r.etudiant_id
        ORDER BY e.id, r.date_fin IS NULL DESC, r.date_fin
    """)
    rows = cursor.fetchall()
    conn.close()

    etudiants_data = {}  # Dictionnaire structurant les données pour chaque étudiant

    for id_, nom, prenom, groupe, ville, date_fin in rows:
        # Si l'étudiant n'est pas encore enregistré dans le dictionnaire
        if id_ not in etudiants_data:
            etudiants_data[id_] = {
                "nom": nom,
                "prenom": prenom,
                "groupe": groupe,
                "ville_principale": None,
                "ville_secondaire": None
            }

        # Classe la résidence comme principale ou secondaire selon la date de fin
        if date_fin is None and etudiants_data[id_]["ville_principale"] is None:
            etudiants_data[id_]["ville_principale"] = ville
        elif date_fin is not None and etudiants_data[id_]["ville_secondaire"] is None:
            etudiants_data[id_]["ville_secondaire"] = ville

    # Conversion du dictionnaire en liste pour affichage
    etudiants = list(etudiants_data.values())

    # Rend la page HTML avec les données des étudiants
    return render_template("etudiants.html", etudiants=etudiants)

# Lance l’application Flask en mode debug si le fichier est exécuté directement
if __name__ == "__main__":
    app.run(debug=True)
