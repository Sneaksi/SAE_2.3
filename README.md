# SAE_2.3

# 🌬️ Ventilomètre des Étudiants — Groupe 15

Projet réalisé dans le cadre de la SAÉ 2.3 du BUT1 Réseaux & Télécommunications.  
Ce projet a été développé par Grégoire JURY--VERMOT DES ROCHES, Florian PISTOLET et Bastien LORENZI.

---

## 🎯 Objectif

Créer une application Web interactive permettant :

- de visualiser les vitesses de vent quotidiennes dans les lieux de résidence des étudiants ;
- d’afficher un **ventilomètre individuel** (résidence principale et secondaire) ;
- de consulter l’**historique** des recherches individuelles et collectives ;
- de calculer le **vent médian collectif du jour**.

---

## 🛠️ Technologies & outils utilisés

- **Python 3** & **Flask** : application Web
- **SQLite** : base de données locale
- **HTML / CSS** : rendu côté client
- **API OpenWeatherMap** : données météorologiques
- **JSON** : données d'import des étudiants

---

## 📁 Arborescence du projet

ventilometre/ ├── templates/ │ ├── etudiants.html # Affiche la liste des étudiants │ └── index.html # Interface principale (formulaire, historique, résultats) ├── app.py # Application Flask ├── collect_wind.py # Récupération des vents via API OpenWeatherMap ├── etudiants.json # Données des étudiants et leurs résidences ├── import_data.py # Import des données JSON vers la base SQLite ├── reset_db.py # Réinitialisation + structure de la base de données ├── students.db # Fichier SQLite (base de données locale)
