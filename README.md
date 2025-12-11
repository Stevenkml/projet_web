# LocaFrance - Version Django

Application de location de logements convertie d'Express.js vers Django.

## Installation

### 1. Prérequis
- Python 3.8+ installé
- pip (gestionnaire de paquets Python)

### 2. Configuration de l'environnement

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows :
venv\Scripts\activate
# Sur Mac/Linux :
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration de la base de données

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur (admin)
python manage.py createsuperuser
```

### 4. Lancer le serveur

```bash
# Démarrer le serveur de développement
python manage.py runserver

# Le site sera accessible sur : http://localhost:8000
# L'interface admin sur : http://localhost:8000/admin
```

## Structure du projet

```
locafrance_django/
├── locafrance_project/       # Configuration principale
│   ├── settings.py           # Configuration Django
│   ├── urls.py               # URLs principales
│   └── wsgi.py
├── accounts/                 # Gestion des utilisateurs
│   ├── models.py             # Modèle User
│   ├── views.py              # Vues API
│   ├── serializers.py        # Sérialiseurs
│   └── urls.py
├── logements/                # Gestion des logements
│   ├── models.py             # Modèles Logement et Avis
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── reservations/             # Gestion des réservations
│   ├── models.py             # Modèle Reservation
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── messages_app/             # Messagerie
├── transports/               # Recherche de transports
├── frontend/                 # Fichiers HTML/CSS/JS
│   ├── index.html
│   ├── pages/
│   ├── css/
│   └── js/
├── requirements.txt          # Dépendances Python
├── .env                      # Variables d'environnement
└── manage.py                 # Script de gestion Django
```

## Modification du frontend

### Mise à jour des URLs API dans api.js

Remplacez `http://localhost:3000/api` par `http://localhost:8000/api` dans le fichier `frontend/js/api.js` :

```javascript
// Configuration de l'API
const API_URL = 'http://localhost:8000/api';
```

### Authentification

Django utilise des tokens d'authentification. Le format reste compatible avec votre frontend existant :

```javascript
headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
}
```

Mais Django REST Framework utilise :

```javascript
headers: {
    'Authorization': `Token ${token}`,  // "Token" au lieu de "Bearer"
    'Content-Type': 'application/json'
}
```

Vous devrez modifier `auth.js` pour changer "Bearer" en "Token".

## Commandes utiles

```bash
# Créer une nouvelle migration après modification des models
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Collecter les fichiers statiques pour production
python manage.py collectstatic

# Lancer les tests
python manage.py test

# Ouvrir le shell Django
python manage.py shell
```

## API Endpoints

### Authentification
- POST `/api/auth/register` - Inscription
- POST `/api/auth/login` - Connexion
- POST `/api/auth/logout` - Déconnexion
- GET/PUT `/api/auth/profil` - Voir/Modifier profil
- PUT `/api/auth/mot-de-passe` - Changer mot de passe

### Logements
- GET `/api/logements/` - Liste des logements
- POST `/api/logements/` - Créer un logement
- GET `/api/logements/{id}/` - Détails d'un logement
- PUT `/api/logements/{id}/` - Modifier un logement
- DELETE `/api/logements/{id}/` - Supprimer un logement

### Réservations
- GET `/api/reservations/` - Mes réservations
- POST `/api/reservations/` - Créer une réservation
- PUT `/api/reservations/{id}/accepter` - Accepter une réservation
- PUT `/api/reservations/{id}/refuser` - Refuser une réservation
- PUT `/api/reservations/{id}/annuler` - Annuler une réservation

## Différences avec la version Node.js

### Base de données
- **Avant (Node.js)** : MySQL avec requêtes SQL brutes
- **Maintenant (Django)** : ORM Django (SQLite par défaut, facilement changeable pour PostgreSQL/MySQL)

### Authentification
- **Avant** : JWT tokens
- **Maintenant** : Django Token Authentication (plus simple)

### Structure
- **Avant** : Routes Express + callbacks
- **Maintenant** : Vues Django REST Framework + serializers

### Avantages de Django
✅ Admin automatique (interface de gestion)
✅ ORM puissant (pas de SQL brut)
✅ Migrations automatiques
✅ Sécurité intégrée (CSRF, XSS, SQL injection)
✅ Documentation automatique avec Django REST Swagger

## Production

Pour déployer en production :

1. Changer `DEBUG = False` dans settings.py
2. Configurer une vraie base de données (PostgreSQL recommandé)
3. Configurer un serveur web (Nginx + Gunicorn)
4. Utiliser des variables d'environnement sécurisées
5. Configurer HTTPS

## Support

Pour toute question, consultez :
- [Documentation Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
