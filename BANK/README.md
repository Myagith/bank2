Exécution rapide
----------------

1) Démarrer PostgreSQL (Docker):

```
docker compose up -d
```

2) Configurer l'environnement:

```
cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

3) Appliquer les migrations et seed:

```
python manage.py migrate
python manage.py loaddata || true
python manage.py seed_demo
```

4) Lancer le serveur:

```
python manage.py runserver 0.0.0.0:8000
```

Comptes de test
---------------
- Admin: admin / Admin123!

Accès DB depuis DBeaver
-----------------------
- Host: localhost
- Port: 5432
- DB: bank_db
- User: bank_user
- Password: bank_pass
