# Importation des modules nécessaires
import json  # Pour lire et manipuler les données JSON
import sqlite3  # Pour interagir avec la base de données SQLite

# Chargement du fichier JSON contenant les étudiants et leurs résidences
with open("etudiants.json", "r", encoding="utf-8") as f:
    etudiants = json.load(f)  # Charge les données sous forme de liste de dictionnaires

# Connexion à la base de données SQLite
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Parcourt chaque étudiant dans le fichier JSON
for etu in etudiants:
    # Mise en forme du nom et prénom
    nom = etu["nom"].upper()  # Nom en majuscules
    prenom = etu["prenom"].capitalize()  # Prénom avec une majuscule en début

    # Récupère le groupe, ou "INCONNU" s'il n'est pas présent dans le JSON
    groupe = etu.get("groupe", "INCONNU")

    # Vérifie si l'étudiant existe déjà dans la base (évite les doublons)
    cursor.execute("SELECT id FROM etudiants WHERE nom = ? AND prenom = ?", (nom, prenom))
    row = cursor.fetchone()

    if row:
        # Si l'étudiant existe déjà, on récupère son ID
        etudiant_id = row[0]
    else:
        # Sinon, on l’insère et on récupère le nouvel ID généré
        cursor.execute("INSERT INTO etudiants (nom, prenom, groupe) VALUES (?, ?, ?)", (nom, prenom, groupe))
        etudiant_id = cursor.lastrowid

    # Parcourt les résidences associées à l'étudiant
    for res in etu["residences"]:
        adresse = res["adresse"]
        ville = res["ville"]
        date_debut = res["date_debut"]
        date_fin = res["date_fin"]

        # Insère chaque résidence dans la base, liée à l'étudiant par son ID
        cursor.execute("""
            INSERT INTO residences (etudiant_id, adresse, ville, date_debut, date_fin)
            VALUES (?, ?, ?, ?, ?)
        """, (etudiant_id, adresse, ville, date_debut, date_fin))

# Sauvegarde les changements dans la base de données
conn.commit()
# Ferme la connexion à la base
conn.close()

# Message de confirmation dans la console
print("Import terminé sans doublons.")
