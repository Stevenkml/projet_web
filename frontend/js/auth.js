// Gestion de l'authentification avec Django

// Vérifier si l'utilisateur est connecté
function isAuthenticated() {
    return localStorage.getItem('token') !== null;
}

// Récupérer les informations de l'utilisateur
function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

// Connexion
async function login(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const credentials = {
        email: formData.get('email'),
        password: formData.get('password')
    };
    
    const errorDiv = document.getElementById('loginError');
    errorDiv.classList.remove('active');
    
    try {
        const response = await AuthAPI.login(credentials);
        
        // Sauvegarder le token et les infos utilisateur
        localStorage.setItem('token', response.token);
        localStorage.setItem('user', JSON.stringify(response.user));
        
        closeModal('loginModal');
        showAlert('Connexion réussie !', 'success');
        updateNavigation();
        
        // Rediriger vers le dashboard
        setTimeout(() => {
            goToDashboard();
        }, 1000);
        
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.classList.add('active');
    }
}

// Inscription
async function register(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const userData = {
        email: formData.get('email'),
        password: formData.get('password'),
        nom: formData.get('nom'),
        prenom: formData.get('prenom'),
        telephone: formData.get('telephone'),
        role: formData.get('role')
    };
    
    const errorDiv = document.getElementById('registerError');
    errorDiv.classList.remove('active');
    
    try {
        const response = await AuthAPI.register(userData);
        
        // Sauvegarder le token et les infos utilisateur
        localStorage.setItem('token', response.token);
        localStorage.setItem('user', JSON.stringify(response.user));
        
        closeModal('registerModal');
        showAlert('Inscription réussie !', 'success');
        updateNavigation();
        
        // Rediriger vers le dashboard
        setTimeout(() => {
            goToDashboard();
        }, 1000);
        
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.classList.add('active');
    }
}

// Déconnexion
async function logout() {
    try {
        // Appeler l'API de déconnexion
        await AuthAPI.logout();
    } catch (error) {
        console.error('Erreur lors de la déconnexion:', error);
    }
    
    // Supprimer les données locales
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    updateNavigation();
    showAlert('Vous êtes déconnecté', 'info');
    
    // Rediriger vers l'accueil
    window.location.href = '/';
}

// Mettre à jour la navigation selon l'état d'authentification
function updateNavigation() {
    const navAuth = document.getElementById('navAuth');
    const navUser = document.getElementById('navUser');

    if (isAuthenticated()) {
        if (navAuth) navAuth.style.display = 'none';
        if (navUser) navUser.style.display = 'flex';
    } else {
        if (navAuth) navAuth.style.display = 'flex';
        if (navUser) navUser.style.display = 'none';
    }
}

// Rediriger vers le dashboard selon le rôle
function goToDashboard() {
    const user = getCurrentUser();
    if (!user) {
        showAlert('Veuillez vous connecter', 'error');
        showLoginModal();
        return;
    }
    
    if (user.role === 'client') {
        window.location.href = '/pages/client-dashboard.html';
    } else if (user.role === 'hote') {
        window.location.href = '/pages/hote-dashboard.html';
    } else if (user.role === 'admin') {
        window.location.href = '/admin';
    }
}

// Afficher modal de connexion
function showLoginModal() {
    document.getElementById('loginModal').classList.add('active');
}

// Afficher modal d'inscription
function showRegisterModal() {
    document.getElementById('registerModal').classList.add('active');
}

// Fermer une modal
function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Vérifier l'accès à une page protégée
function requireAuth(requiredRole = null) {
    if (!isAuthenticated()) {
        showAlert('Vous devez être connecté pour accéder à cette page', 'error');
        setTimeout(() => {
            window.location.href = '../index.html';
        }, 1500);
        return false;
    }
    
    if (requiredRole) {
        const user = getCurrentUser();
        if (user.role !== requiredRole) {
            showAlert('Accès non autorisé', 'error');
            setTimeout(() => {
                window.location.href = '../index.html';
            }, 1500);
            return false;
        }
    }
    
    return true;
}

// Initialiser l'état de la navigation au chargement
document.addEventListener('DOMContentLoaded', () => {
    updateNavigation();
    
    // Gérer le clic en dehors des modals
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.classList.remove('active');
        }
    });
});
