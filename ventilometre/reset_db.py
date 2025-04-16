import os
import sqlite3
import json

# === 1. Supprimer la base de données si elle existe déjà ===
if os.path.exists("students.db"):
    os.remove("students.db")  # Supprime le fichier "students.db"
    print("🗑️ Ancienne base supprimée.")

# === 2. Création d’une nouvelle base de données ===
conn = sqlite3.connect("students.db")  # Crée un nouveau fichier de base de données
cursor = conn.cursor()  # Initialise un curseur pour exécuter des requêtes SQL

# Création de la table des étudiants
cursor.execute("""
CREATE TABLE IF NOT EXISTS etudiants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    groupe TEXT
)
""")

# Création de la table des résidences associées à chaque étudiant
cursor.execute("""
CREATE TABLE IF NOT EXISTS residences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    etudiant_id INTEGER NOT NULL,
    adresse TEXT NOT NULL,
    ville TEXT NOT NULL,
    date_debut TEXT NOT NULL,
    date_fin TEXT,
    FOREIGN KEY (etudiant_id) REFERENCES etudiants(id)
)
""")

# Création de la table contenant les données météo associées à chaque résidence
cursor.execute("""
CREATE TABLE IF NOT EXISTS meteo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    residence_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    vent REAL,
    FOREIGN KEY (residence_id) REFERENCES residences(id)
)
""")

# Création de la table pour l’historique des recherches
cursor.execute("""
CREATE TABLE IF NOT EXISTS historique_recherches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    ville1 TEXT,
    vent1 REAL,
    ville2 TEXT,
    vent2 REAL,
    heure TEXT
)
""")

print("✅ Nouvelle base créée avec toutes les colonnes.")

# === 3. Importation des données depuis le fichier JSON ===
with open("etudiants.json", "r", encoding="utf-8") as f:
    data = json.load(f)  # Chargement des données JSON en mémoire

# Parcourt chaque étudiant dans les données JSON
for etu in data:
    # Insertion de l’étudiant dans la table `etudiants`
    cursor.execute("INSERT INTO etudiants (nom, prenom, groupe) VALUES (?, ?, ?)",
                   (etu["nom"], etu["prenom"], etu["groupe"]))
    etudiant_id = cursor.lastrowid  # Récupère l’ID automatiquement généré

    # Insertion des résidences associées à cet étudiant
    for res in etu["residences"]:
        cursor.execute("""
            INSERT INTO residences (etudiant_id, adresse, ville, date_debut, date_fin)
            VALUES (?, ?, ?, ?, ?)
        """, (etudiant_id, res["adresse"], res["ville"], res["date_debut"], res["date_fin"]))

# Sauvegarde les modifications dans la base
conn.commit()
# Ferme la connexion à la base de données
conn.close()

# Message de confirmation
print("📥 Import terminé avec groupes et résidences.")