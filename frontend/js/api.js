// Configuration de l'API Django
const API_URL = 'http://localhost:8000/api';

// Fonction utilitaire pour les requêtes API
async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        // Django utilise "Token" au lieu de "Bearer"
        headers['Authorization'] = `Token ${token}`;
    }
    
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || data.detail || 'Une erreur est survenue');
        }
        
        return data;
    } catch (error) {
        console.error('Erreur API:', error);
        throw error;
    }
}

// API Auth
const AuthAPI = {
    async register(userData) {
        return await apiRequest('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    },
    
    async login(credentials) {
        return await apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
    },
    
    async logout() {
        return await apiRequest('/auth/logout', {
            method: 'POST'
        });
    }
};

// API Logements
const LogementsAPI = {
    async getAll(filters = {}) {
        const params = new URLSearchParams(filters);
        return await apiRequest(`/logements/?${params}`);
    },
    
    async getById(id) {
        return await apiRequest(`/logements/${id}/`);
    },
    
    async create(logementData) {
        return await apiRequest('/logements/', {
            method: 'POST',
            body: JSON.stringify(logementData)
        });
    },
    
    async update(id, logementData) {
        return await apiRequest(`/logements/${id}/`, {
            method: 'PUT',
            body: JSON.stringify(logementData)
        });
    },
    
    async delete(id) {
        return await apiRequest(`/logements/${id}/`, {
            method: 'DELETE'
        });
    },
    
    async getMesLogements() {
        return await apiRequest('/logements/hote/mes-logements/');
    }
};

// API Réservations
const ReservationsAPI = {
    async create(reservationData) {
        return await apiRequest('/reservations/', {
            method: 'POST',
            body: JSON.stringify(reservationData)
        });
    },
    
    async getMesReservations() {
        return await apiRequest('/reservations/client/mes-reservations/');
    },
    
    async getMesReservationsHote() {
        return await apiRequest('/reservations/hote/mes-reservations/');
    },
    
    async accepter(id) {
        return await apiRequest(`/reservations/${id}/accepter/`, {
            method: 'PUT'
        });
    },
    
    async refuser(id) {
        return await apiRequest(`/reservations/${id}/refuser/`, {
            method: 'PUT'
        });
    },
    
    async annuler(id) {
        return await apiRequest(`/reservations/${id}/annuler/`, {
            method: 'PUT'
        });
    },
    
    async addAvis(reservationId, avisData) {
        return await apiRequest(`/reservations/${reservationId}/avis/`, {
            method: 'POST',
            body: JSON.stringify(avisData)
        });
    }
};

// API Transports
const TransportsAPI = {
    async rechercherTrajets(depart, arrivee, date) {
        const params = new URLSearchParams({ depart, arrivee, date });
        return await apiRequest(`/transports/trajets/?${params}`);
    },
    
    async getVilles(recherche = '') {
        const params = recherche ? `?recherche=${recherche}` : '';
        return await apiRequest(`/transports/villes${params}`);
    }
};

// API Users
const UsersAPI = {
    async getProfil() {
        return await apiRequest('/auth/profil');
    },
    
    async updateProfil(userData) {
        return await apiRequest('/auth/profil', {
            method: 'PUT',
            body: JSON.stringify(userData)
        });
    },
    
    async changePassword(passwordData) {
        return await apiRequest('/auth/mot-de-passe', {
            method: 'PUT',
            body: JSON.stringify(passwordData)
        });
    }
};

// Fonction pour afficher les alertes
function showAlert(message, type = 'info') {
    // Supprimer les alertes existantes
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    
    const icon = type === 'success' ? 'check-circle' : 
                 type === 'error' ? 'exclamation-circle' : 
                 'info-circle';
    
    alert.innerHTML = `
        <i class="fas fa-${icon}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 5000);
}
