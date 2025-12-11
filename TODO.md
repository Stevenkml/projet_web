# 📝 TODO - LocaFrance Django

## ✅ Déjà fait

- [x] Structure du projet Django
- [x] Modèle User personnalisé
- [x] API d'authentification (register, login, logout)
- [x] Modèle Logement avec avis
- [x] Modèle Reservation
- [x] Configuration CORS
- [x] Configuration REST Framework
- [x] Interface admin
- [x] Documentation d'installation
- [x] Scripts d'installation automatique

## 🔄 À compléter

### Backend Django (Prioritaire)

#### 1. Logements (logements/views.py)
- [ ] LogementListView - Lister tous les logements avec filtres
- [ ] LogementDetailView - Détails d'un logement
- [ ] LogementCreateView - Créer un logement (hôte uniquement)
- [ ] LogementUpdateView - Modifier un logement (hôte uniquement)
- [ ] LogementDeleteView - Supprimer un logement (hôte uniquement)
- [ ] MesLogementsView - Logements de l'hôte connecté
- [ ] LogementSerializer - Sérialiseur pour les logements
- [ ] AvisListView - Liste des avis d'un logement

#### 2. Réservations (reservations/views.py)
- [ ] ReservationCreateView - Créer une réservation
- [ ] MesReservationsClientView - Réservations du client
- [ ] MesReservationsHoteView - Réservations reçues (hôte)
- [ ] AccepterReservationView - Accepter une réservation
- [ ] RefuserReservationView - Refuser une réservation
- [ ] AnnulerReservationView - Annuler une réservation
- [ ] CreerAvisView - Créer un avis après réservation
- [ ] ReservationSerializer - Sérialiseur pour réservations

#### 3. Messagerie (messages_app/)
- [ ] Créer le modèle Message
- [ ] ConversationListView - Liste des conversations
- [ ] MessageListView - Messages d'une conversation
- [ ] SendMessageView - Envoyer un message
- [ ] MarkAsReadView - Marquer comme lu
- [ ] MessageSerializer

#### 4. Transports (transports/views.py)
- [ ] RechercherTrajetsView - Rechercher des trajets
- [ ] VillesListView - Liste des villes
- [ ] IntégrationAPI externe (optionnel)

#### 5. Admin (admin.py pour chaque app)
- [ ] LogementAdmin - Configuration admin logements
- [ ] ReservationAdmin - Configuration admin réservations
- [ ] AvisAdmin - Configuration admin avis
- [ ] MessageAdmin - Configuration admin messages

### Frontend

#### Modifications nécessaires
- [ ] Changer `localhost:3000` → `localhost:8000` dans api.js
- [ ] Changer `Bearer` → `Token` dans auth.js et api.js
- [ ] Copier tous les fichiers HTML/CSS/JS dans `frontend/`
- [ ] Tester toutes les pages

#### Nouveaux fichiers à créer (optionnel)
- [ ] Utiliser les templates Django au lieu de HTML statique
- [ ] Créer des formulaires Django pour l'admin

### Tests

- [ ] Tests unitaires pour les modèles
- [ ] Tests pour l'API d'authentification
- [ ] Tests pour l'API logements
- [ ] Tests pour l'API réservations
- [ ] Tests pour la messagerie
- [ ] Tests d'intégration

### Déploiement

- [ ] Configuration pour production (DEBUG=False)
- [ ] Migrer vers PostgreSQL
- [ ] Configuration Nginx
- [ ] Configuration Gunicorn
- [ ] Variables d'environnement sécurisées
- [ ] Configuration HTTPS/SSL
- [ ] Sauvegarde automatique base de données

### Fonctionnalités additionnelles

- [ ] Upload d'images pour les logements
- [ ] Système de paiement (Stripe/PayPal)
- [ ] Notifications email
- [ ] Recherche avancée avec ElasticSearch
- [ ] API de géolocalisation
- [ ] Calendrier de disponibilité
- [ ] Système de favoris
- [ ] Export de données (PDF/CSV)
- [ ] Dashboard avec statistiques

### Documentation

- [ ] Documentation API avec Swagger/OpenAPI
- [ ] Guide utilisateur
- [ ] Guide de contribution
- [ ] Changelog

### Sécurité

- [ ] Limiter le nombre de requêtes (rate limiting)
- [ ] Validation avancée des données
- [ ] Audit de sécurité
- [ ] Tests de pénétration
- [ ] Configuration Content Security Policy

## 📋 Ordre de développement recommandé

### Phase 1 : Backend de base (1-2 jours)
1. Compléter logements/views.py
2. Compléter reservations/views.py
3. Tester l'API avec Postman/curl

### Phase 2 : Frontend (1 jour)
1. Modifier api.js et auth.js
2. Copier les fichiers frontend
3. Tester l'intégration

### Phase 3 : Messagerie (1 jour)
1. Créer modèle Message
2. Créer les vues
3. Tester

### Phase 4 : Transports (0.5 jour)
1. Adapter transports.js vers Django
2. Tester

### Phase 5 : Polish & Tests (1 jour)
1. Tests unitaires
2. Correction bugs
3. Amélioration UX

### Phase 6 : Déploiement (1 jour)
1. Configuration production
2. Déploiement sur serveur
3. Tests en production

## 🎯 MVP (Minimum Viable Product)

Pour avoir un site fonctionnel rapidement, prioriser :

**Backend MVP :**
- ✅ Auth (déjà fait)
- [ ] CRUD Logements (2h)
- [ ] CRUD Réservations (2h)
- [ ] Messagerie basique (2h)

**Frontend MVP :**
- [ ] Modifier URLs API (30 min)
- [ ] Tester pages principales (1h)

**Total MVP : ~8 heures de développement**

## 📞 Besoin d'aide ?

Consultez :
- README.md - Vue d'ensemble
- INSTALLATION.md - Guide d'installation détaillé
- QUICKSTART.md - Démarrage rapide
- COMPARISON.md - Différences Node.js vs Django

## 🐛 Bugs connus

- Aucun pour le moment (projet neuf)

## 💡 Idées futures

- [ ] Application mobile (React Native/Flutter)
- [ ] Progressive Web App (PWA)
- [ ] Support multilingue (i18n)
- [ ] Chat en temps réel (WebSockets/Channels)
- [ ] Intelligence artificielle pour recommandations
- [ ] Intégration calendrier (Google Calendar, iCal)
- [ ] Programme de fidélité
- [ ] Parrainage
