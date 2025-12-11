# 🎉 LocaFrance Django - PRÊT À L'EMPLOI !

## ✅ Ce que contient cette archive

Une application Django **complètement configurée** avec :
- ✅ Base de données SQLite créée
- ✅ Migrations appliquées
- ✅ Comptes de test créés
- ✅ Données de démonstration
- ✅ Interface admin fonctionnelle

## ⚡ Démarrage en 30 secondes

```bash
# 1. Extraire l'archive
unzip locafrance_django_ready.zip
cd locafrance_django

# 2. Installer les dépendances (une seule fois)
pip install -r requirements.txt

# 3. Lancer le serveur
python manage.py runserver

# 4. Ouvrir dans le navigateur
# http://localhost:8000/admin
```

## 🔐 Comptes disponibles

### Admin (tout accès)
- Email: `admin@locafrance.fr`
- Mot de passe: `admin123`

### Hôte (avec logements)
- Email: `hote@test.fr`
- Mot de passe: `test123`

### Client
- Email: `client@test.fr`
- Mot de passe: `test123`

## 📁 Fichiers importants

```
📄 START_HERE.md     ⭐ COMMENCEZ PAR CE FICHIER
📄 QUICKSTART.md     Guide de démarrage rapide
📄 INSTALLATION.md   Installation détaillée
📄 TODO.md           Ce qu'il reste à faire
📄 COMPARISON.md     Différences Node.js vs Django
```

## 🚀 Ce qui fonctionne déjà

- ✅ Authentification API (login, register, profil)
- ✅ Interface admin complète
- ✅ Modèles de données (User, Logement, Reservation, Avis)
- ✅ Base de données avec données de test
- ✅ 3 logements de démonstration

## 📋 Ce qu'il reste à faire (~10h)

1. Compléter les vues API pour logements (2h)
2. Compléter les vues API pour réservations (2h)
3. Adapter votre frontend (2h)
4. Système de messagerie (2h)
5. Recherche de transports (1h)
6. Tests (1h)

**Détails complets dans TODO.md**

## 🌐 URLs importantes

Après avoir lancé `python manage.py runserver` :

- **Interface Admin:** http://localhost:8000/admin
- **API Auth:** http://localhost:8000/api/auth/
- **Site web:** http://localhost:8000

## 💡 Exemples d'utilisation

### Test API avec curl

```bash
# Connexion
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"client@test.fr","password":"test123"}'

# Retourne un token
# {"token":"abc123...","user":{...}}

# Voir son profil
curl http://localhost:8000/api/auth/profil \
  -H "Authorization: Token abc123..."
```

### Explorer dans l'admin Django

1. Aller sur http://localhost:8000/admin
2. Se connecter avec admin@locafrance.fr / admin123
3. Cliquer sur "Utilisateurs" pour voir tous les comptes
4. Cliquer sur "Logements" pour voir les 3 logements de test
5. Modifier, ajouter ou supprimer des éléments

## 🎯 Avantages vs Node.js

| Fonctionnalité | Node.js Express | Django |
|----------------|-----------------|--------|
| Interface admin | ❌ À créer (8h+) | ✅ Incluse (0h) |
| ORM | ❌ SQL manuel | ✅ ORM Python |
| Sécurité | ⚠️ À configurer | ✅ Par défaut |
| Temps de dev | ~15h | ~5h |

## 🐛 Problèmes ?

### Module Django non trouvé
```bash
pip install -r requirements.txt --break-system-packages
```

### Port 8000 déjà utilisé
```bash
python manage.py runserver 8080
```

### Mot de passe admin oublié
```bash
python manage.py changepassword admin@locafrance.fr
```

## 📞 Support

Consultez les fichiers de documentation inclus :
- START_HERE.md - Guide complet
- QUICKSTART.md - Démarrage rapide
- INSTALLATION.md - Installation détaillée

## 🎓 Apprendre Django

- Documentation officielle : https://docs.djangoproject.com/
- Django Girls Tutorial : https://tutorial.djangogirls.org/fr/
- Real Python : https://realpython.com/tutorials/django/

---

**🚀 Prêt ? Lancez `python manage.py runserver` et visitez http://localhost:8000/admin !**
