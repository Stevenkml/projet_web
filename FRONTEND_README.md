# 🎨 FRONTEND LOCAFRANCE - COMPLET ET FONCTIONNEL

## ✅ Ce qui est inclus

### 📄 Pages HTML
- ✅ **index.html** - Page d'accueil avec recherche
- ✅ **client-dashboard.html** - Dashboard client
- ✅ **logement-details.html** - Détails d'un logement avec réservation

### 🎨 CSS
- ✅ **style.css** - Styles complets et responsive
  - Variables CSS
  - Navigation
  - Hero section
  - Cards logements
  - Formulaires
  - Modals
  - Responsive design

### ⚙️ JavaScript
- ✅ **api.js** - API adaptée pour Django
  - URL Django (localhost:8000)
  - Token Auth (Token au lieu de Bearer)
  - Toutes les fonctions API

- ✅ **auth.js** - Authentification complète
  - Login/Logout
  - Register
  - Gestion du token
  - Navigation dynamique

- ✅ **app.js** - Logique de l'application
  - Chargement des logements
  - Filtres de recherche
  - Affichage des cards

## 🔄 Différences avec la version Node.js

### URLs API
```javascript
// ❌ AVANT (Node.js)
const API_URL = 'http://localhost:3000/api';

// ✅ MAINTENANT (Django)
const API_URL = 'http://localhost:8000/api';
```

### Format du token
```javascript
// ❌ AVANT (JWT)
'Authorization': `Bearer ${token}`

// ✅ MAINTENANT (Django Token)
'Authorization': `Token ${token}`
```

### Chemins des fichiers statiques
```html
<!-- ❌ AVANT -->
<link rel="stylesheet" href="css/style.css">
<script src="js/api.js"></script>

<!-- ✅ MAINTENANT -->
<link rel="stylesheet" href="/static/css/style.css">
<script src="/static/js/api.js"></script>
```

## 🚀 Comment tester

### 1. Lancer le serveur Django
```bash
cd locafrance_django
python manage.py runserver
```

### 2. Ouvrir dans le navigateur
```
http://localhost:8000
```

### 3. Tester les fonctionnalités

#### Page d'accueil (/)
- ✅ Formulaire de recherche
- ✅ Affichage des logements
- ✅ Filtres
- ✅ Navigation

#### Se connecter
- Email: client@test.fr
- Mot de passe: test123

#### Voir un logement
- Cliquer sur une carte de logement
- Voir les détails
- Faire une réservation

#### Dashboard client
- Après connexion : /pages/client-dashboard.html
- Voir les réservations

## 📂 Structure des fichiers

```
frontend/
├── index.html              # Page d'accueil
├── css/
│   └── style.css          # Styles complets
├── js/
│   ├── api.js             # API Django
│   ├── auth.js            # Authentification
│   └── app.js             # Logique app
└── pages/
    ├── client-dashboard.html    # Dashboard client
    └── logement-details.html    # Détails logement
```

## 🎯 Fonctionnalités frontend

### ✅ Implémentées
- [x] Page d'accueil avec hero
- [x] Recherche de logements
- [x] Filtres avancés
- [x] Affichage des logements en grille
- [x] Page détails logement
- [x] Formulaire de réservation
- [x] Authentification (login/register)
- [x] Dashboard client
- [x] Navigation responsive
- [x] Modals
- [x] Alertes

### ⏳ À ajouter (optionnel)
- [ ] Dashboard hôte
- [ ] Gestion des logements (hôte)
- [ ] Messagerie
- [ ] Recherche de transports
- [ ] Upload de photos
- [ ] Galerie d'images

## 🎨 Design

### Couleurs
- **Primary:** #007bff (bleu)
- **Success:** #28a745 (vert)
- **Danger:** #dc3545 (rouge)
- **Warning:** #ffc107 (jaune)

### Typographie
- **Font:** System fonts (-apple-system, Segoe UI, Roboto)
- **Responsive:** 768px breakpoint

### Composants
- Cards logements
- Formulaires modernes
- Boutons avec hover effects
- Navigation sticky
- Footer complet

## 🔧 Configuration Django pour le frontend

Dans `settings.py` :
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend'],
        ...
    }
]

STATICFILES_DIRS = [
    BASE_DIR / 'frontend',
]
```

Dans `urls.py` :
```python
from django.views.generic import TemplateView

urlpatterns = [
    ...
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]
```

## 💡 Exemples d'utilisation

### Rechercher des logements
```javascript
// Depuis n'importe quelle page
await LogementsAPI.getAll({ ville: 'Paris', prix_max: 100 });
```

### Se connecter
```javascript
await AuthAPI.login({ email: 'client@test.fr', password: 'test123' });
```

### Réserver un logement
```javascript
await ReservationsAPI.create({
    logement_id: 1,
    date_debut: '2025-01-01',
    date_fin: '2025-01-05',
    nombre_voyageurs: 2,
    prix_total: 260.00
});
```

## 🐛 Problèmes courants

### Les styles ne se chargent pas
```bash
# Collecter les fichiers statiques
python manage.py collectstatic
```

### Erreur CORS
Vérifier dans `settings.py` :
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
]
```

### Les images ne s'affichent pas
Les URLs d'images utilisent unsplash.com par défaut.
Pour utiliser vos propres images, modifiez les URLs dans la base de données.

## 📱 Responsive

Le frontend est entièrement responsive :
- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1199px)
- ✅ Mobile (< 768px)

### Menu mobile
- Hamburger menu sur mobile
- Navigation adaptative
- Touch-friendly

## ⚡ Performance

### Optimisations
- CSS minifié
- Lazy loading des images
- Fetch API moderne
- Pas de jQuery (vanilla JS)

### Chargement
- Styles inline pour le critical CSS
- Scripts en fin de body
- Images avec placeholder

## 🎯 Prochaines améliorations

1. **Dashboard hôte** (2h)
   - Créer/modifier logements
   - Gérer réservations

2. **Messagerie** (2h)
   - Chat en temps réel
   - Notifications

3. **Upload photos** (1h)
   - Galerie d'images
   - Multiple photos par logement

4. **Recherche avancée** (1h)
   - Autocomplete villes
   - Carte interactive

5. **Profil utilisateur** (1h)
   - Modifier profil
   - Avatar
   - Préférences

## ✨ Résumé

Vous avez maintenant un frontend complet et moderne pour LocaFrance :
- ✅ Design professionnel
- ✅ Responsive
- ✅ Intégré avec Django
- ✅ Prêt pour la production

**Il ne reste plus qu'à compléter les vues API backend ! (voir TODO.md)**
