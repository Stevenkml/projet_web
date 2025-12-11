# 🔄 COMPARAISON : Node.js Express → Django

## Vue d'ensemble

| Aspect | Node.js Express | Django |
|--------|----------------|--------|
| **Langage** | JavaScript | Python |
| **Framework Web** | Express.js | Django |
| **Framework API** | Custom | Django REST Framework |
| **Base de données** | MySQL (avec requêtes SQL) | SQLite/PostgreSQL (avec ORM) |
| **Auth** | JWT manuel | Django Token Auth |
| **Admin** | Aucun | Interface admin automatique |
| **Port par défaut** | 3000 | 8000 |

## Correspondance des fichiers

### Backend

| Fichier Node.js | Équivalent Django | Description |
|----------------|-------------------|-------------|
| `server.js` | `manage.py` + `settings.py` | Configuration serveur |
| `routes/auth.js` | `accounts/views.py` + `accounts/urls.py` | Routes d'authentification |
| `routes/logements.js` | `logements/views.py` + `logements/urls.py` | Routes logements |
| `routes/reservations.js` | `reservations/views.py` + `reservations/urls.py` | Routes réservations |
| `routes/messages.js` | `messages_app/views.py` + `messages_app/urls.py` | Routes messagerie |
| `routes/transports.js` | `transports/views.py` + `transports/urls.py` | Routes transports |
| `middleware/auth.js` | `rest_framework.authentication` | Middleware auth |
| N/A | `*/models.py` | Modèles de données (ORM) |
| N/A | `*/serializers.py` | Validation/sérialisation |
| N/A | `*/admin.py` | Interface admin |

### Frontend

| Fichier | Modification nécessaire |
|---------|------------------------|
| `js/api.js` | ✏️ Changer URL : `localhost:3000` → `localhost:8000` |
| `js/auth.js` | ✏️ Changer token : `Bearer` → `Token` |
| Autres fichiers | ✅ Aucune modification |

## Exemples de code côte à côte

### 1. Création d'un utilisateur

**Node.js Express :**
```javascript
// routes/auth.js
router.post('/register', async (req, res) => {
  const { email, password, nom, prenom } = req.body;
  const hashedPassword = await bcrypt.hash(password, 10);
  
  await db.query(
    'INSERT INTO users (email, password, nom, prenom) VALUES (?, ?, ?, ?)',
    [email, hashedPassword, nom, prenom]
  );
  
  const token = jwt.sign({ userId: result.insertId }, SECRET_KEY);
  res.json({ token, user: {...} });
});
```

**Django :**
```python
# accounts/views.py
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
```

### 2. Récupération de logements

**Node.js Express :**
```javascript
// routes/logements.js
router.get('/', async (req, res) => {
  const { ville, prix_max } = req.query;
  
  let query = 'SELECT * FROM logements WHERE 1=1';
  const params = [];
  
  if (ville) {
    query += ' AND ville = ?';
    params.push(ville);
  }
  if (prix_max) {
    query += ' AND prix_par_nuit <= ?';
    params.push(prix_max);
  }
  
  const logements = await db.query(query, params);
  res.json(logements);
});
```

**Django :**
```python
# logements/views.py
class LogementListView(generics.ListAPIView):
    serializer_class = LogementSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Logement.objects.all()
        
        ville = self.request.query_params.get('ville')
        prix_max = self.request.query_params.get('prix_max')
        
        if ville:
            queryset = queryset.filter(ville__icontains=ville)
        if prix_max:
            queryset = queryset.filter(prix_par_nuit__lte=prix_max)
        
        return queryset
```

### 3. Middleware d'authentification

**Node.js Express :**
```javascript
// middleware/auth.js
const authMiddleware = async (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    return res.status(401).json({ error: 'Non autorisé' });
  }
  
  try {
    const decoded = jwt.verify(token, SECRET_KEY);
    const user = await db.query('SELECT * FROM users WHERE id = ?', [decoded.userId]);
    req.user = user;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Token invalide' });
  }
};
```

**Django :**
```python
# Configuration automatique dans settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Utilisation dans les vues :
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # L'utilisateur est automatiquement disponible via self.request.user
```

## Avantages de Django

### ✅ Ce que vous gagnez

1. **Admin automatique**
   - Interface de gestion complète sans code
   - CRUD automatique pour tous les modèles
   - Personnalisable facilement

2. **ORM puissant**
   - Plus de SQL brut à écrire
   - Requêtes type-safe
   - Migrations automatiques

3. **Sécurité intégrée**
   - Protection CSRF automatique
   - Protection XSS
   - Protection SQL injection
   - Hashage sécurisé des mots de passe

4. **Validation des données**
   - Validation automatique via serializers
   - Messages d'erreur cohérents
   - Type checking

5. **Documentation API**
   - Interface Browsable API gratuite
   - Swagger/OpenAPI facile à ajouter

6. **Écosystème riche**
   - Packages Django bien maintenus
   - Grande communauté
   - Beaucoup de tutoriels

### 🔄 Ce que vous devez adapter

1. **Syntaxe**
   - JavaScript → Python
   - Callbacks/Promises → Async/Await Python

2. **Structure**
   - Routes Express → Vues Django
   - Middleware custom → Permissions/Authentication classes

3. **Base de données**
   - SQL brut → ORM Django
   - Gestion manuelle des transactions → Transactions automatiques

4. **Token format**
   - `Bearer ${token}` → `Token ${token}`

5. **URL patterns**
   - Express: `router.get('/users/:id')` 
   - Django: `path('users/<int:pk>/')`

## Temps de développement

| Tâche | Node.js Express | Django |
|-------|----------------|--------|
| Setup initial | 30 min | 15 min |
| Modèles de données | 1h (SQL) | 30 min (ORM) |
| Routes CRUD | 2h | 1h (avec DRF) |
| Interface admin | 4-8h | 0h (automatique) |
| Auth système | 2-3h | 30 min |
| Tests | 2h | 1h |
| **TOTAL** | **~12h** | **~3h** |

## Performance

### Node.js Express
- ⚡ Très rapide pour I/O
- 🔄 Async naturel
- 📦 Léger en mémoire

### Django
- 🐍 Légèrement plus lent (Python)
- 🔄 Async disponible (depuis Django 3.1)
- 📦 Plus gourmand en mémoire
- ⚡ Suffisamment rapide pour 99% des cas

## Migration progressive

Vous pouvez migrer progressivement :

```
Étape 1: Garder Node.js, utiliser Django uniquement pour l'admin
        Node.js (port 3000) ← Frontend
        Django (port 8000) ← Admin uniquement

Étape 2: Migrer l'API petit à petit
        Node.js (certaines routes)
        Django (nouvelles routes)

Étape 3: Migration complète
        Django uniquement
```

## Conclusion

### Choisir Node.js Express si :
- ❤️ Vous préférez JavaScript
- ⚡ Vous avez besoin de performances extrêmes
- 🔄 Vous faites du temps réel intensif (WebSockets)
- 🎯 Vous voulez un contrôle total

### Choisir Django si :
- 🐍 Vous préférez Python
- 🚀 Vous voulez développer vite
- 👥 Vous avez besoin d'un admin
- 🛡️ Vous privilégiez la sécurité
- 📚 Vous voulez des conventions établies

### Pour LocaFrance :
Django est un excellent choix car :
- ✅ Interface admin pour gérer logements/users
- ✅ ORM pour requêtes complexes (recherche, filtres)
- ✅ Sécurité critique (paiements futurs)
- ✅ Développement rapide
- ✅ Évolutivité facile
