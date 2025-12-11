# 🚀 VOTRE SITE EST PRÊT !

## ✅ Installation terminée avec succès

Votre application LocaFrance Django est maintenant configurée et contient des données de test.

## 🔐 Comptes de test disponibles

### Administrateur (accès complet)
- **Email:** admin@locafrance.fr
- **Mot de passe:** admin123
- **Accès:** Interface admin + API complète

### Hôte (peut créer des logements)
- **Email:** hote@test.fr
- **Mot de passe:** test123
- **Rôle:** Hôte avec 3 logements déjà créés

### Client (peut réserver)
- **Email:** client@test.fr
- **Mot de passe:** test123
- **Rôle:** Client

## 🌐 Démarrer le serveur

```bash
cd locafrance_django
python manage.py runserver
```

Le serveur démarre sur : **http://localhost:8000**

## 🎯 Pages à tester

### Interface Admin Django
**URL:** http://localhost:8000/admin
**Login:** admin@locafrance.fr / admin123

Vous pouvez :
- ✅ Gérer tous les utilisateurs
- ✅ Gérer tous les logements
- ✅ Voir les statistiques
- ✅ Modifier les données
- ✅ Supprimer des éléments

### API Endpoints disponibles

#### Authentification
```bash
# Inscription
POST http://localhost:8000/api/auth/register
{
    "email": "nouveau@test.fr",
    "password": "test123",
    "nom": "Test",
    "prenom": "User",
    "role": "client"
}

# Connexion
POST http://localhost:8000/api/auth/login
{
    "email": "client@test.fr",
    "password": "test123"
}
# Retourne: { "token": "...", "user": {...} }

# Profil
GET http://localhost:8000/api/auth/profil
Headers: Authorization: Token YOUR_TOKEN_HERE
```

## 📊 Données de test créées

- ✅ 1 administrateur
- ✅ 1 hôte (Sophie Martin)
- ✅ 1 client (Pierre Dubois)
- ✅ 3 logements :
  - Studio cosy Paris 11ème (65€/nuit)
  - Appartement lumineux Lyon (90€/nuit)
  - Villa avec piscine Marseille (250€/nuit)

## 🔄 Prochaines étapes

### 1. Tester l'admin (5 minutes)
```bash
# Démarrer le serveur
python manage.py runserver

# Ouvrir dans le navigateur
http://localhost:8000/admin

# Se connecter avec admin@locafrance.fr / admin123
# Explorer les sections Users, Logements, etc.
```

### 2. Tester l'API (avec Postman ou curl)

**Test de connexion :**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"client@test.fr","password":"test123"}'
```

**Récupérer son profil :**
```bash
curl http://localhost:8000/api/auth/profil \
  -H "Authorization: Token VOTRE_TOKEN"
```

### 3. Copier votre frontend

```bash
# Copier vos fichiers HTML/CSS/JS dans le dossier frontend/
cp votre_index.html frontend/
cp -r votre_css/ frontend/css/
cp -r votre_js/ frontend/js/
cp -r votre_pages/ frontend/pages/

# Modifier frontend/js/api.js
# Changer: const API_URL = 'http://localhost:8000/api';

# Modifier frontend/js/auth.js
# Changer: 'Authorization': `Token ${token}`
```

### 4. Compléter les vues API (TODO.md)

Les modèles sont créés, maintenant il faut ajouter les vues pour :
- [ ] Liste des logements avec filtres
- [ ] Créer/modifier/supprimer un logement
- [ ] Créer/gérer des réservations
- [ ] Système de messagerie

## 🛠️ Commandes utiles

```bash
# Créer un nouveau user
python manage.py createsuperuser

# Ouvrir le shell Django
python manage.py shell

# Voir les migrations
python manage.py showmigrations

# Créer des migrations après modification des models
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic
```

## 📱 Structure de la base de données

### Tables créées

1. **users** - Utilisateurs (clients, hôtes, admins)
2. **logements** - Logements disponibles
3. **reservations** - Réservations
4. **avis** - Avis sur les logements
5. **authtoken_token** - Tokens d'authentification
6. + tables Django standards (sessions, permissions, etc.)

## 🎨 Personnalisation

### Changer la langue de l'admin
Dans `settings.py` :
```python
LANGUAGE_CODE = 'fr-fr'  # Déjà configuré
```

### Ajouter des champs à un modèle
1. Modifier le fichier `models.py`
2. Créer une migration : `python manage.py makemigrations`
3. Appliquer : `python manage.py migrate`

### Personnaliser l'interface admin
Modifier le fichier `admin.py` de chaque app

## 🐛 Dépannage

### Le serveur ne démarre pas
```bash
# Vérifier que Django est installé
python -c "import django; print(django.get_version())"

# Réinstaller si nécessaire
pip install -r requirements.txt --break-system-packages
```

### Erreur "Table doesn't exist"
```bash
# Recréer les migrations
python manage.py makemigrations
python manage.py migrate
```

### Oublié le mot de passe admin
```bash
python manage.py changepassword admin@locafrance.fr
```

## 📚 Documentation

- **Django:** https://docs.djangoproject.com/
- **Django REST Framework:** https://www.django-rest-framework.org/
- **Fichiers du projet:**
  - README.md - Vue d'ensemble
  - QUICKSTART.md - Guide rapide
  - INSTALLATION.md - Installation détaillée
  - COMPARISON.md - Différences Node.js vs Django
  - TODO.md - Liste des tâches

## ✨ Félicitations !

Votre application Django est opérationnelle. Vous avez :
- ✅ Une base de données configurée
- ✅ Des modèles de données créés
- ✅ Une interface admin fonctionnelle
- ✅ Une API REST avec authentification
- ✅ Des données de test pour commencer

**Prêt à coder ? Consultez TODO.md pour voir ce qu'il reste à faire ! 🚀**
