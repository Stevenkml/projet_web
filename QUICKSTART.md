# 🚀 GUIDE DE DÉMARRAGE RAPIDE - LocaFrance Django

## ⚡ Installation en 5 minutes

### Option 1 : Installation automatique (Recommandé)

**Windows :**
```cmd
install.bat
```

**Mac/Linux :**
```bash
chmod +x install.sh
./install.sh
```

### Option 2 : Installation manuelle

```bash
# 1. Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer la base de données
python manage.py makemigrations
python manage.py migrate

# 4. Créer un admin
python manage.py createsuperuser

# 5. Lancer le serveur
python manage.py runserver
```

## 📂 Structure des fichiers

```
locafrance_django/
│
├── 📁 locafrance_project/      # Configuration Django
│   ├── settings.py             # ⚙️ Configuration
│   ├── urls.py                 # 🔗 Routes principales
│   └── wsgi.py
│
├── 📁 accounts/                # 👤 Gestion utilisateurs
│   ├── models.py               # User personnalisé
│   ├── views.py                # API auth
│   ├── serializers.py
│   └── urls.py
│
├── 📁 logements/               # 🏠 Gestion logements
│   ├── models.py               # Logement, Avis
│   └── urls.py
│
├── 📁 reservations/            # 📅 Gestion réservations
│   ├── models.py               # Reservation
│   └── urls.py
│
├── 📁 messages_app/            # 💬 Messagerie
│   └── urls.py
│
├── 📁 transports/              # 🚗 Recherche transports
│   └── urls.py
│
├── 📁 frontend/                # 🎨 Fichiers HTML/CSS/JS
│   ├── index.html
│   ├── pages/
│   ├── css/
│   └── js/
│
├── manage.py                   # 🔧 Commandes Django
├── requirements.txt            # 📦 Dépendances
├── .env                        # 🔐 Variables d'environnement
└── README.md                   # 📖 Documentation
```

## 🔄 Modifications nécessaires dans votre frontend

### 1. Changer l'URL de l'API

**Dans `frontend/js/api.js` :**
```javascript
// ❌ AVANT (Node.js)
const API_URL = 'http://localhost:3000/api';

// ✅ APRÈS (Django)
const API_URL = 'http://localhost:8000/api';
```

### 2. Changer le format du token d'authentification

**Dans `frontend/js/auth.js` et `frontend/js/api.js` :**

Cherchez toutes les occurrences de :
```javascript
'Authorization': `Bearer ${token}`
```

Et remplacez par :
```javascript
'Authorization': `Token ${token}`
```

**Exemple complet dans api.js :**
```javascript
async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Token ${token}`;  // ← Changement ici !
    }
    
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Une erreur est survenue');
        }
        
        return data;
    } catch (error) {
        console.error('Erreur API:', error);
        throw error;
    }
}
```

## 📋 Checklist de migration

- [ ] Python 3.8+ installé
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Migrations appliquées (`python manage.py migrate`)
- [ ] Superutilisateur créé (`python manage.py createsuperuser`)
- [ ] Frontend copié dans le dossier `frontend/`
- [ ] URL API changée dans `api.js` (localhost:8000)
- [ ] Format token changé (Bearer → Token)
- [ ] Serveur lancé (`python manage.py runserver`)
- [ ] Site accessible sur http://localhost:8000
- [ ] Admin accessible sur http://localhost:8000/admin

## 🧪 Tester l'installation

### 1. Vérifier que le serveur fonctionne
```bash
python manage.py runserver
```
→ Ouvrir http://localhost:8000

### 2. Tester l'admin Django
→ Ouvrir http://localhost:8000/admin
→ Se connecter avec le superutilisateur

### 3. Tester l'API
```bash
# Test de l'endpoint de santé
curl http://localhost:8000/api/auth/register
```

### 4. Créer des données de test

**Via l'admin (recommandé) :**
1. Aller sur http://localhost:8000/admin
2. Créer des utilisateurs (Hôtes et Clients)
3. Créer des logements
4. Créer des réservations

**Via le shell Django :**
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
    password='test123',
    nom='Martin',
    prenom='Sophie',
    role='hote'
)

# Créer un logement
logement = Logement.objects.create(
    hote=hote,
    titre='Studio cosy Paris 11ème',
    description='Charmant studio refait à neuf',
    type='studio',
    adresse='25 rue Oberkampf',
    ville='Paris',
    code_postal='75011',
    prix_par_nuit=65.00,
    capacite_max=2,
    nombre_chambres=1,
    nombre_salles_bain=1,
    wifi=True,
    cuisine=True
)

print(f"✅ Logement créé : {logement.titre}")
```

## 🆘 Problèmes courants et solutions

### Problème : "ModuleNotFoundError: No module named 'django'"
**Cause :** L'environnement virtuel n'est pas activé
**Solution :**
```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### Problème : "django.db.utils.OperationalError: no such table"
**Cause :** Les migrations n'ont pas été appliquées
**Solution :**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Problème : CORS errors dans la console du navigateur
**Cause :** Configuration CORS incorrecte
**Solution :** Vérifier dans `settings.py` :
```python
INSTALLED_APPS = [
    ...
    'corsheaders',  # ← Doit être présent
]

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',  # ← Avant CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
```

### Problème : "Access denied for user 'root'@'localhost'"
**Cause :** Problème de configuration base de données
**Solution :** Par défaut, Django utilise SQLite (pas de config nécessaire)

### Problème : Les fichiers statiques (CSS/JS) ne se chargent pas
**Solution :**
```bash
python manage.py collectstatic
```

## 🎯 Commandes essentielles

```bash
# Démarrer le serveur
python manage.py runserver

# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Ouvrir le shell Django
python manage.py shell

# Vérifier les erreurs
python manage.py check

# Collecter les fichiers statiques
python manage.py collectstatic
```

## 🔗 URLs importantes

- **Site web :** http://localhost:8000
- **Admin Django :** http://localhost:8000/admin
- **API Auth :** http://localhost:8000/api/auth/
- **API Logements :** http://localhost:8000/api/logements/
- **API Réservations :** http://localhost:8000/api/reservations/

## 📚 Documentation

- Django : https://docs.djangoproject.com/
- Django REST Framework : https://www.django-rest-framework.org/
- Tutoriel Django : https://tutorial.djangogirls.org/fr/

## ✅ Prochaines étapes

1. ✅ Installation de base terminée
2. ⏭️ Compléter les vues API pour logements
3. ⏭️ Compléter les vues API pour réservations
4. ⏭️ Implémenter la messagerie
5. ⏭️ Implémenter la recherche de transports
6. ⏭️ Tests
7. ⏭️ Déploiement en production

---

**Besoin d'aide ?** Consultez les fichiers README.md et INSTALLATION.md pour plus de détails !
