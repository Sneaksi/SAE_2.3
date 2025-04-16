# Importation des modules nécessaires
import sqlite3  # Pour interagir avec la base de données SQLite
import requests  # Pour faire des requêtes HTTP à l'API météo
from datetime import date  # Pour récupérer la date du jour

# Clé API personnelle pour OpenWeatherMap
API_KEY = "a8509ca3fb0936444107b801b3edab07"
# URL de l’API météo pour récupérer les données actuelles d'une ville
API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Fonction pour récupérer la vitesse du vent d'une ville
def get_wind(ville):
    try:
        # Envoie une requête à l’API météo avec la ville, la clé API, l’unité en °C, et la langue en français
        res = requests.get(API_URL, params={
            "q": ville,
            "appid": API_KEY,
            "units": "metric",
            "lang": "fr"
        })
        # Retourne la vitesse du vent en m/s extraite de la réponse JSON
        return res.json()['wind']['speed']
    except:
        # En cas d’erreur (ville inconnue, problème réseau...), retourne None
        return None

# Récupère la date d’aujourd’hui au format ISO (YYYY-MM-DD)
today = date.today().isoformat()

# Connexion à la base de données
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Récupère toutes les résidences (id + nom de ville)
cursor.execute("SELECT id, ville FROM residences")
residences = cursor.fetchall()

# Parcourt chaque résidence pour insérer les données de vent du jour
for res_id, ville in residences:
    # Vérifie si une donnée météo a déjà été insérée pour cette résidence aujourd’hui
    cursor.execute("SELECT 1 FROM meteo WHERE residence_id = ? AND date = ?", (res_id, today))
    if cursor.fetchone() is None:
        # Si ce n’est pas le cas, récupère la vitesse du vent via l’API
        vent = get_wind(ville)
        # Insère les données météo dans la table meteo
        cursor.execute("INSERT INTO meteo (residence_id, date, vent) VALUES (?, ?, ?)", (res_id, today, vent))

# Sauvegarde les changements dans la base de données
conn.commit()
# Ferme la connexion
conn.close()

# Affiche un message de confirmation dans la console
print("✅ Données de vent enregistrées pour le jour :", today)
