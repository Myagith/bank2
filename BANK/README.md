# Bank - Application Django

## Vue d'ensemble
Application bancaire avec authentification par rôles (ADMIN, CLIENT), dashboards dédiés, gestion banques/clients/comptes/transactions, facturation PDF et envoi d'emails, protections middleware et contrôle d'accès par rôle.

## Pile technique
- Python 3.10+
- Django 5.2
- PostgreSQL 16 (via Docker Compose fourni)
- django-filter, xhtml2pdf, Pillow, ReportLab
- Chart.js (via CDN) pour les graphiques

## Fonctionnalités clés
- Utilisateur personnalisé `users.User` (hérite d'`AbstractUser`) avec `role ∈ {ADMIN, CLIENT}`
- Connexion/Déconnexion; redirection par rôle
- Forçage de changement de mot de passe au premier login
- Middleware global (login requis) + décorateur `@role_required` pour les rôles
- Dashboard Admin: KPIs globaux, top-15 banques, graphiques, stats par banque de l’admin, transactions récentes
- Dashboard Client: infos perso, comptes, solde global, transactions récentes, graphiques dépôts vs retraits
- Gestion: Banques (filtres pays/ville, top-15), Clients (recherche), Comptes (ouverture/fermeture/closing), Transactions (validation métier)
- Factures (PDF) et envoi email (signals)
- Commande `createusers` (ADMIN/CLIENT par défaut)

## Prérequis
- Python 3.10+ et pip
- Docker et Docker Compose (recommandé pour Postgres) OU PostgreSQL installé localement

## Installation (Python)
```bash
python3.10 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r BANK/requirements.txt
```

## Base de données
### Option A (recommandé): Docker Compose
```bash
cd BANK
docker compose up -d db
```
La base est exposée sur `127.0.0.1:5432` avec:
- DB: `bank_db`
- USER: `bank_user`
- PASS: `bank_pass`

### Option B: PostgreSQL local
Créez la base/utilisateur et alignez les variables suivantes (ou modifiez `bank/settings.py`):
```
POSTGRES_DB=bank_db
POSTGRES_USER=bank_user
POSTGRES_PASSWORD=bank_pass
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

## Migrations et données de base
```bash
cd BANK
python manage.py migrate
python manage.py createusers
```
Crée par défaut:
- ADMIN: `admin / admin123`
- CLIENT: `client / client123`

## Lancer l'application
```bash
python manage.py runserver 0.0.0.0:8000
```

## URLs principales
- Auth: `/auth/login/`, `/auth/logout/`, `/auth/dashboard/`
- Dashboards: `/auth/dashboard/admin/`, `/auth/dashboard/client/`
- Banques: `/banks/`, `/banks/top-15/`, `/banks/<id>/clients/`
- Clients: `/customers/`
- Comptes: `/accounts/` (+ `/<id>/close/`, `/<id>/closing/`)
- Transactions: `/transactions/create/`, `/transactions/history/`
- Facturation: `/billing/create/`, `/billing/<id>/send/`
- Admin Django: `/admin/`

Accès:
- ADMIN: accès complet + dashboard admin
- CLIENT: accès limité + dashboard client

## Emails et PDF
- Environnements de dev: email en console (config par défaut)
- Signals:
  - Création Banque → email de bienvenue propriétaire
  - Création Client → email de bienvenue
  - Création Facture → email avec PDF en PJ
- Templates d’emails: `templates/emails/`

## Médias & statiques
- Médias uploadés: `BANK/media` (configuré via `MEDIA_ROOT`)
- Statiques: `BANK/static`

## Commandes utiles
```bash
# Créer utilisateurs par défaut
python manage.py createusers

# Créer seulement un client personnalisé
python manage.py shell -c "from django.contrib.auth import get_user_model; U=get_user_model(); u=U.objects.create_user(username='client2', password='pass123', role='CLIENT'); u.can_login=True; u.save()"
```

## Dépannage
- Erreur de connexion DB: vérifiez que Postgres est démarré (Docker) et variables `.env`/settings
- Problèmes d’installation pip: installez dépendances système: `build-essential libffi-dev libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev`

## Licence
Projet de démonstration interne.