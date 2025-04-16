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

```
ventilometre/
├── templates/
│   ├── etudiants.html        # Affiche la liste des étudiants
│   └── index.html            # Interface principale (formulaire, historique, résultats)
├── app.py                    # Application Flask
├── collect_wind.py           # Récupération des vents via API OpenWeatherMap
├── etudiants.json            # Données des étudiants et leurs résidences
├── import_data.py            # Import des données JSON vers la base SQLite
├── reset_db.py               # Réinitialisation + structure de la base de données
├── students.db               # Fichier SQLite (base de données locale)
```

---

## 🚀 Installation rapide

### 1. Cloner le dépôt

```bash
git clone https://github.com/<ton-utilisateur>/ventilometre-g15.git
cd ventilometre-g15
```

### 2. Créer et activer un environnement virtuel (recommandé)

```bash
python -m venv env
source env/bin/activate   # ou env\Scripts\activate sur Windows
```

### 3. Installer les dépendances

```bash
pip install flask requests
```

### 4. Lancer l’application

```bash
python reset_db.py        # Réinitialise la base de données
python import_data.py     # Importe les données depuis le fichier JSON
python collect_wind.py    # Récupère les vents du jour
python app.py             # Lance le serveur Flask
```

---

## 🧪 Fonctionnalités principales

1. 🔍 **Recherche d’un étudiant** : saisie du nom → affichage du vent dans ses lieux de résidence.
2. 🧾 **Historique** : journal des recherches globales et personnelles.
3. 🌍 **Vent médian collectif** : calcul automatique à partir de toutes les résidences du jour.
4. 📋 **Liste des étudiants** : toutes les résidences et groupes accessibles en un clic.

---

## 👥 Répartition de l'équipe

- **Grégoire JURY--VERMOT DES ROCHES** : architecture backend, base de données, API météo.
- **Florian PISTOLET** : gestion des données, import JSON/SQL, scripts automatiques.
- **Bastien LORENZI** : design HTML/CSS, vues utilisateurs, ergonomie.

---

## 💡 Notes supplémentaires

- Les résidences sont datées (`date_debut`, `date_fin`), permettant un tri logique entre résidence principale (active) et secondaire (ancienne).
- Le code est commenté et structuré pour faciliter la maintenance.
- L'application est conçue pour un usage local mais peut être déployée sur un serveur avec peu de modifications.

---

## 📷 Aperçu visuel

Ajoutez ici vos captures d'écran dans un dossier `/screenshots/` pour illustrer l'app.

---

## 📚 Licence

Projet pédagogique — pas de licence officielle.  
Reproduction autorisée dans le cadre de la formation BUT Réseaux & Télécoms.

---

## 📬 Contact

Pour toute question :  
📧 jury-vermot.gr@gmail.com  bastienlorenzi70@gmail.com 
🧑‍💻 GitHub : [https://github.com/Sneaksi/SAE_2.3/blob/main/README.md]
