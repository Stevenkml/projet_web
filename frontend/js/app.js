// Variables globales
let logementsData = [];
let currentFilters = {};

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

// Initialiser l'application
async function initApp() {
    // Définir la date minimale pour les recherches (aujourd'hui)
    const today = new Date().toISOString().split('T')[0];
    const dateDebutInput = document.getElementById('searchDateDebut');
    const dateFinInput = document.getElementById('searchDateFin');
    
    if (dateDebutInput) dateDebutInput.min = today;
    if (dateFinInput) dateFinInput.min = today;
    
    // Gérer le menu mobile
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }
    
    // Charger les logements au démarrage
    await chargerLogements();
}

// Charger les logements
async function chargerLogements(filters = {}) {
    const logementsGrid = document.getElementById('logementsGrid');
    const loading = document.getElementById('loading');
    const noResults = document.getElementById('noResults');
    
    if (!logementsGrid) return;
    
    try {
        loading.style.display = 'block';
        noResults.style.display = 'none';
        logementsGrid.innerHTML = '';
        
        const response = await LogementsAPI.getAll(filters);
        
        // 🐛 DEBUG - Afficher la réponse complète
        console.log('🔍 Réponse API brute:', response);
        console.log('🔍 Type de response:', typeof response);
        console.log('🔍 Est un tableau?', Array.isArray(response));
        console.log('🔍 response.results existe?', response.results);
        
        // Django REST Framework peut retourner un objet avec results ou directement un tableau
        const logements = Array.isArray(response) ? response : (response.results || []);
        
        console.log('✅ Logements extraits:', logements);
        console.log('✅ Nombre de logements:', logements.length);
        
        logementsData = logements;
        
        loading.style.display = 'none';
        
        if (logements.length === 0) {
            noResults.style.display = 'block';
            return;
        }
        
        logements.forEach(logement => {
            const card = createLogementCard(logement);
            logementsGrid.appendChild(card);
        });
        
    } catch (error) {
        loading.style.display = 'none';
        showAlert('Erreur lors du chargement des logements', 'error');
        console.error('Erreur détaillée:', error);
    }
}

// Créer une carte de logement
function createLogementCard(logement) {
    // 🐛 DEBUG
    console.log('Création carte logement:', logement.id, logement.titre);
    
    const card = document.createElement('a');
    card.href = `/pages/logement-details.html?id=${logement.id}`;
    card.className = 'logement-card';
    
    const noteAffichage = logement.note_moyenne 
        ? `<div class="logement-rating">
             <i class="fas fa-star"></i>
             <span>${parseFloat(logement.note_moyenne).toFixed(1)}</span>
             <span>(${logement.nombre_avis})</span>
           </div>`
        : '<div class="logement-rating"><span>Nouveau</span></div>';
    
    card.innerHTML = `
        <img src="${logement.photo_url || 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400'}" 
             alt="${logement.titre}" 
             class="logement-image"
             onerror="this.src='https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400'">
        <div class="logement-content">
            <div class="logement-header">
                <div>
                    <h3 class="logement-title">${logement.titre}</h3>
                    <p class="logement-location">
                        <i class="fas fa-map-marker-alt"></i> ${logement.ville}
                    </p>
                </div>
                ${noteAffichage}
            </div>
            
            <div class="logement-details">
                <span><i class="fas fa-bed"></i> ${logement.nombre_chambres} ch.</span>
                <span><i class="fas fa-user"></i> ${logement.capacite_max} pers.</span>
                <span><i class="fas fa-bath"></i> ${logement.nombre_salles_bain} sdb.</span>
            </div>
            
            <div class="logement-price">
                ${logement.prix_par_nuit}€ <span>/ nuit</span>
            </div>
            
            <span class="logement-badge">${getTypeLabel(logement.type)}</span>
        </div>
    `;
    
    return card;
}

// Obtenir le label du type de logement
function getTypeLabel(type) {
    const labels = {
        'appartement': 'Appartement',
        'maison': 'Maison',
        'studio': 'Studio',
        'villa': 'Villa',
        'chambre': 'Chambre'
    };
    return labels[type] || type;
}

// Rechercher des logements
async function rechercherLogements() {
    const ville = document.getElementById('searchVille').value;
    const dateDebut = document.getElementById('searchDateDebut').value;
    const dateFin = document.getElementById('searchDateFin').value;
    const voyageurs = document.getElementById('searchVoyageurs').value;
    
    currentFilters = {};
    
    if (ville) currentFilters.ville = ville;
    if (dateDebut) currentFilters.date_debut = dateDebut;
    if (dateFin) currentFilters.date_fin = dateFin;
    if (voyageurs) currentFilters.capacite = voyageurs;
    
    // Afficher la section de filtres
    const filtersSection = document.getElementById('filtersSection');
    if (filtersSection && Object.keys(currentFilters).length > 0) {
        filtersSection.style.display = 'block';
    }
    
    // Mettre à jour le titre des résultats
    const resultsTitle = document.getElementById('resultsTitle');
    if (resultsTitle) {
        if (ville) {
            resultsTitle.textContent = `Logements à ${ville}`;
        } else {
            resultsTitle.textContent = 'Résultats de recherche';
        }
    }
    
    await chargerLogements(currentFilters);
    
    // Scroll vers les résultats
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

// Appliquer les filtres avancés
async function appliquerFiltres() {
    const type = document.getElementById('filterType').value;
    const prixMax = document.getElementById('filterPrixMax').value;
    const capacite = document.getElementById('filterCapacite').value;
    
    if (type) currentFilters.type = type;
    if (prixMax) currentFilters.prix_max = prixMax;
    if (capacite) currentFilters.capacite = capacite;
    
    await chargerLogements(currentFilters);
}

// Calculer le nombre de nuits entre deux dates
function calculerNuits(dateDebut, dateFin) {
    const debut = new Date(dateDebut);
    const fin = new Date(dateFin);
    const diffTime = Math.abs(fin - debut);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
}

// Formater une date en français
function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
    });
}

// Formater le statut de réservation
function getStatutLabel(statut) {
    const labels = {
        'en_attente': { text: 'En attente', class: 'warning' },
        'acceptee': { text: 'Acceptée', class: 'success' },
        'refusee': { text: 'Refusée', class: 'danger' },
        'annulee': { text: 'Annulée', class: 'secondary' }
    };
    return labels[statut] || { text: statut, class: 'secondary' };
}

// Exporter les fonctions globales
window.rechercherLogements = rechercherLogements;
window.appliquerFiltres = appliquerFiltres;