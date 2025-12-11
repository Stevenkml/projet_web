# GUIDE D'INSTALLATION COMPLET - LocaFrance Django

## Étape 1 : Installation de Python

### Windows
1. Téléchargez Python depuis https://www.python.org/downloads/
2. Cochez "Add Python to PATH" pendant l'installation
3. Vérifiez l'installation :
```cmd
python --version
```

### Mac
```bash
# Installer Homebrew si pas déjà fait
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installer Python
brew install python3
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

## Étape 2 : Créer la structure du projet

```bash
# Créer le dossier principal
mkdir locafrance_django
cd locafrance_django

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows :
venv\Scripts\activate
# Sur Mac/Linux :
source venv/bin/activate

# Vous devriez voir (venv) devant votre prompt
```

## Étape 3 : Installer les dépendances

```bash
# Installer Django et les packages nécessaires
pip install Django==5.0
pip install djangorestframework==3.14.0
pip install django-cors-headers==4.3.1
pip install python-decouple==3.8
pip install Pillow==10.2.0

# Ou installer depuis requirements.txt
pip install -r requirements.txt
```

## Étape 4 : Créer le projet Django

```bash
# Créer le projet principal
django-admin startproject locafrance_project .

# Créer les applications
python manage.py startapp accounts
python manage.py startapp logements
python manage.py startapp reservations
python manage.py startapp messages_app
python manage.py startapp transports
```

## Étape 5 : Copier les fichiers fournis

Copiez tous les fichiers que je vous ai fournis dans leurs dossiers respectifs :

```
locafrance_django/
├── manage.py
├── requirements.txt
├── .env
├── README.md
├── locafrance_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── logements/
│   ├── __init__.py
│   └── models.py
└── reservations/
    ├── __init__.py
    └── models.py
```

## Étape 6 : Copier votre frontend

```bash
# Créer le dossier frontend
mkdir frontend
mkdir frontend/css
mkdir frontend/js
mkdir frontend/pages

# Copier vos fichiers HTML/CSS/JS existants
# - index.html → frontend/
# - style.css → frontend/css/
# - api.js, auth.js, app.js → frontend/js/
# - pages HTML → frontend/pages/
```

## Étape 7 : Modifier votre frontend pour Django

### Dans `frontend/js/api.js`, changez l'URL de l'API :

```javascript
// AVANT (Node.js)
const API_URL = 'http://localhost:3000/api';

// APRÈS (Django)
const API_URL = 'http://localhost:8000/api';
```

### Dans `frontend/js/auth.js`, changez le format du token :

```javascript
// AVANT (JWT)
headers: {
    'Authorization': `Bearer ${token}`
}

// APRÈS (Django Token)
headers: {
    'Authorization': `Token ${token}`
}
```

## Étape 8 : Configuration de la base de données

```bash
# Créer les tables de la base de données
python manage.py makemigrations
python manage.py migrate

# Créer un compte administrateur
python manage.py createsuperuser
# Entrez : email, nom, prénom, mot de passe
```

## Étape 9 : Tester le serveur

```bash
# Démarrer le serveur de développement
python manage.py runserver

# Ouvrir dans votre navigateur :
# Site web : http://localhost:8000
# Admin : http://localhost:8000/admin
```

## Étape 10 : Créer des données de test

### Via l'interface admin (http://localhost:8000/admin)

1. Connectez-vous avec votre compte superutilisateur
2. Créez des utilisateurs (clients et hôtes)
3. Créez des logements
4. Créez des réservations

### Via le shell Django

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from logements.models import Logement
User = get_user_model()

# Créer un hôte
hote = User.objects.create_user(
    email='hote@test.com',
    password='password123',
    nom='Dupont',
    prenom='Marie',
    role='hote'
)

# Créer un logement
logement = Logement.objects.create(
    hote=hote,
    titre='Appartement cosy à Paris',
    description='Bel appartement lumineux',
    type='appartement',
    adresse='10 rue de la Paix',
    ville='Paris',
    code_postal='75001',
    prix_par_nuit=80.00,
    capacite_max=4,
    nombre_chambres=2,
    nombre_salles_bain=1,
    wifi=True,
    parking=True
)
```

## Problèmes courants

### Erreur : "ModuleNotFoundError: No module named 'django'"
**Solution** : L'environnement virtuel n'est pas activé
```bash
# Réactiver l'environnement
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### Erreur : "django.core.exceptions.ImproperlyConfigured"
**Solution** : Vérifiez que INSTALLED_APPS dans settings.py contient toutes vos apps

### Erreur : "CORS header 'Access-Control-Allow-Origin'"
**Solution** : Vérifiez que 'corsheaders' est dans INSTALLED_APPS et MIDDLEWARE

### Le CSS ne se charge pas
**Solution** : 
```bash
python manage.py collectstatic
```

## Commandes utiles

```bash
# Voir toutes les migrations
python manage.py showmigrations

# Annuler la dernière migration
python manage.py migrate app_name previous_migration

# Créer un nouveau superuser
python manage.py createsuperuser

# Vérifier les erreurs du projet
python manage.py check

# Ouvrir le shell Django
python manage.py shell

# Vider la base de données
python manage.py flush
```

## Développement vs Production

### En développement (actuel)
- DEBUG = True
- SQLite database
- Serveur de développement Django

### En production (à configurer plus tard)
- DEBUG = False
- PostgreSQL ou MySQL
- Gunicorn + Nginx
- Variables d'environnement sécurisées
- HTTPS

## Prochaines étapes

1. ✅ Installation de base
2. ⏭️ Compléter les vues et sérialiseurs pour logements
3. ⏭️ Compléter les vues pour réservations
4. ⏭️ Implémenter la messagerie
5. ⏭️ Implémenter la recherche de transports
6. ⏭️ Tests
7. ⏭️ Déploiement

## Ressources

- Documentation Django : https://docs.djangoproject.com/
- Django REST Framework : https://www.django-rest-framework.org/
- Django pour débutants : https://tutorial.djangogirls.org/fr/
