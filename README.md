# Hotelin-Tsika - Version Web

Application web de gestion hoteliere, reproduisant l'interface du logiciel desktop PyQt5 dans un navigateur.

## Fonctionnalites

### Gestion des Clients
- Ajout, modification et suppression de clients
- Validation des donnees (CIN 12 chiffres, telephone 10 chiffres, email, dates)
- Attribution automatique de chambres (VIP 1-20, Classic 1-50)
- Detection de conflits de reservation
- Calcul automatique du nombre de nuits et de la recette
- Recherche en temps reel
- Export CSV

### Gestion du Personnel
- Recrutement, modification de grade, absence, paiement, licenciement
- Calcul automatique du salaire (base x coefficient du grade)
- Deduction automatique des absences (toutes les 5 absences : -15%)
- Suivi du dernier paiement

### Archives
- Archivage automatique des clients dont la date de depart est passee
- Historique complet avec date d'archivage
- Vide d'archives

### Interface
- Theme sombre inspire de l'application desktop
- Popups de notification personnalisees
- Messages flash avec animation

## Technologies

- **Backend** : Python / Flask
- **Base de donnees** : PostgreSQL
- **Frontend** : HTML, CSS, JavaScript
- **Authentification** : Sessions Flask + hashage des mots de passe

## Deploiement sur Render

Le projet est pre-configurer avec `render.yaml`. Pour deployer :

1. Pousser le code sur GitHub
2. Creer un compte sur [render.com](https://render.com)
3. New > Blueprint > Connecter le repo GitHub
4. Render detecte automatiquement `render.yaml` et cree la base PostgreSQL + l'app web

L'application sera accessible sur `https://hotelin-tsika-web.onrender.com`

## Installation locale

### Pre requis
- Python 3.10+
- PostgreSQL
- `uv` (ou `pip`)

### Etapes

```bash
# Cloner le projet
git clone https://github.com/aimee-randrianandrasana/Hotelin-Tsika-Web.git
cd Hotelin-Tsika-Web

# Creer l'environnement virtuel
uv venv .venv
source .venv/bin/activate

# Installer les dependances
uv pip install -r requirements.txt

# Configurer la base de donnees
cp .env.example .env
# Modifier DATABASE_URL dans .env selon votre configuration PostgreSQL

# Lancer l'application
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## Configuration

Fichier `.env` :

```env
DATABASE_URL=postgresql://user:password@localhost/hotel_tsika
SECRET_KEY=votre_cle_secrete
ADMIN_USER=joker@gmail.com
ADMIN_PASS=joker@test
```

## Structure du projet

```
Hotelin-Tsika-Web/
├── app.py                  # Point d'entree Flask
├── config.py               # Configuration et constantes
├── db.py                   # Connexion et creation des tables
├── render.yaml             # Configuration Render (deploiement)
├── requirements.txt        # Dependances Python
├── .env                    # Variables d'environnement
├── models/
│   ├── client.py           # Modele client (CRUD)
│   └── employee.py         # Modele employe (CRUD)
├── services/
│   ├── client_service.py   # Logique metier clients
│   └── employee_service.py # Logique metier employes
├── routes/
│   ├── auth.py             # Connexion / deconnexion
│   ├── clients.py          # Routes clients
│   ├── employees.py        # Routes employes
│   └── archives.py         # Routes archives
├── utils/
│   └── helpers.py          # Validations et utilitaires
├── templates/
│   ├── base.html           # Layout principal (sidebar + popups)
│   ├── login.html          # Page de connexion
│   ├── dashboard.html      # Tableau de bord
│   ├── clients.html        # Gestion des clients
│   ├── employees.html      # Gestion du personnel
│   └── archives.html       # Archives
└── static/
    ├── css/style.css       # Styles globaux
    └── js/app.js           # Recherche globale
```

## Auteur

**Randrianandrasana Jean Aime**
- GitHub : [aimee-randrianandrasana](https://github.com/aimee-randrianandrasana)

## Licence

Projet academique - ENI Madagascar
