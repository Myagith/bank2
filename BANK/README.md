## Payguard Banque – Plateforme de gestion bancaire (Django)

Application Django complète avec utilisateur personnalisé, rôles ADMIN/CLIENT, middleware d’authentification globale, dashboards par rôle, opérations bancaires, exports et données de démonstration.

### Démonstration rapide
- URL: `http://localhost:8000/users/login/`
- Identifiants ADMIN: `admin / Admin123!`

### Pile technique
- Django 5, PostgreSQL (Docker Compose), psycopg, django-filter
- Chart.js pour les graphiques, CSS custom (thème orange → blanc → vert)
- Emails via backend console (par défaut) ou SMTP via `.env`

## Installation

### Prérequis
- Python 3.11+ (recommandé), Docker + Docker Compose, Git

### 1) Cloner
```bash
git clone https://github.com/Myagith/bank.git
cd bank
```

### 2) Environnement Python
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Variables d’environnement
```bash
cp .env.example .env
```
Variables clés (.env):
- `POSTGRES_DB=bank_db`
- `POSTGRES_USER=bank_user`
- `POSTGRES_PASSWORD=bank_pass`
- `POSTGRES_HOST=postgres` (via Docker) ou `127.0.0.1`
- `POSTGRES_PORT=5432`
- `EMAIL_BACKEND` (par défaut console), `DEFAULT_FROM_EMAIL`

### 4) Base de données (Docker)
```bash
docker compose up -d
```

### 5) Migrations + données de démo
```bash
python manage.py migrate
python manage.py seed_demo
```

### 6) Lancer le serveur
```bash
python manage.py runserver 0.0.0.0:8000
```

## Rôles et sécurité
- CustomUser (`users.User`) avec champ `role ∈ {ADMIN, CLIENT}`
- Pas d’inscription publique: création par ADMIN uniquement
- Login/Logout + OTP email (6 chiffres) après login
- Middleware global `core.RequireAuthenticationMiddleware`:
  - autorise: `/users/login`, `/users/logout`, `/users/otp`, `/admin`, `/static`, `/media`
  - redirige toute autre page vers login si non authentifié
- Redirection post‑login: ADMIN → dashboard admin, CLIENT → dashboard client

## Fonctionnalités principales
- Dashboard ADMIN:
  - Statistiques globales: banques, clients, comptes (ouverts/fermés)
  - Transactions récentes, graphique mensuel
  - Top 15 banques par nombre de clients + filtres (année, min clients)
  - Exports CSV/Excel des Top banques

- Espace CLIENT:
  - Aperçu solde global (démo), accès à ses comptes/transactions
  - Graphique Dépenses vs Dépôts (démo)

- Comptes/Transactions:
  - Liste/filtrage comptes, création/modification
  - Création d’opérations (dépôt/retrait/transfer) + email de notification

## Données de démo
Commande: `python manage.py seed_demo`
- 15 banques (ex: Banque Atlantique, SG CI, NSIA, BOA, UBA, …)
- ~30 clients, 1–2 comptes chacun, plusieurs transactions
- 1 superadmin: `admin / Admin123!`

## Exports
- Dashboard → boutons:
  - CSV: `/dashboard/export/top-banks.csv`
  - Excel: `/dashboard/export/top-banks.xlsx`

## Emails
- Par défaut, console: les emails (OTP, bienvenue) s’affichent dans le terminal

### Configuration e‑mail SMTP (Gmail)
1) Active un “App Password” sur ton compte Google (Sécurité → Mots de passe d’application).
2) Mets à jour `.env` (déjà pré‑rempli dans `.env.example`):
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=votre.email@gmail.com
EMAIL_HOST_PASSWORD=VOTRE_APP_PASSWORD
EMAIL_USE_TLS=1
EMAIL_USE_SSL=0
DEFAULT_FROM_EMAIL=votre.email@gmail.com

# Personnalisation des messages
BANK_NAME=PAYGUARD
OTP_EMAIL_SUBJECT=PAYGUARD - Votre code de connexion
OTP_EMAIL_BODY=Bonjour {username},\n\nVotre code de connexion est: {code}.\nIl expire dans {expires_minutes} minutes.\n\n{app_name}
WELCOME_EMAIL_SUBJECT=Bienvenue sur PAYGUARD
WELCOME_EMAIL_BODY=Bonjour {username},\n\nVotre compte a été créé.\nIdentifiant: {username}\nMot de passe initial: {password}\n\nMerci d'utiliser {app_name}.

# Démo: OTP fixe (désactiver en prod)
DEFAULT_OTP_CODE=123456
```
3) Redémarre le serveur.

## Structure du projet (extrait)
```
bank/
  bank/                 # settings, urls
  users/                # CustomUser, auth/OTP, admin-only register
  banks/                # Modèles/CRUD banques
  customers/            # Clients (rattachés aux banques)
  accounts/             # Comptes (client, type, solde, statut)
  transactions/         # Transactions + services
  dashboard/            # Vues, API, exports CSV/XLSX
  core/                 # Middleware, seed_demo
  templates/            # Templates par app, base, dashboard
  static/css/theme.css  # Thème UI
  docker-compose.yml    # PostgreSQL
  .env.example          # Variables d’environnement
```

## Connexion à la base (DBeaver)
- Host: `localhost`
- Port: `5432`
- Database: `bank_db`
- User: `bank_user`
- Password: `bank_pass`

## Commandes utiles
```bash
# Créer un superadmin manuel (optionnel)
python manage.py createsuperuser

# Collecte des fichiers statiques (prod)
python manage.py collectstatic

# Export de données (exemples)
python manage.py dumpdata banks > banks.json
python manage.py loaddata banks.json
```

## Dépannage
- Port 5432 déjà utilisé: stoppe l’autre Postgres, ou change le port dans `docker-compose.yml` et `.env`
- Problème d’OTP non reçu: en mode console, le code apparaît dans le terminal; en SMTP, vérifie tes identifiants
- Erreur de migration: `python manage.py migrate --plan` puis `python manage.py migrate`

## Licence
Projet de démonstration pour présentation interne. Adapter avant mise en production.
