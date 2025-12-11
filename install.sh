#!/bin/bash

echo "==================================="
echo "Installation de LocaFrance Django"
echo "==================================="
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "ERREUR : Python 3 n'est pas installé !"
    echo "Installez Python 3 :"
    echo "  - Mac: brew install python3"
    echo "  - Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

echo "[1/6] Python détecté !"
echo ""

# Créer l'environnement virtuel
echo "[2/6] Création de l'environnement virtuel..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERREUR : Impossible de créer l'environnement virtuel"
    exit 1
fi

# Activer l'environnement virtuel
echo "[3/6] Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "[4/6] Installation des dépendances..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERREUR : Installation des dépendances échouée"
    exit 1
fi

# Créer la base de données
echo "[5/6] Configuration de la base de données..."
python manage.py makemigrations
python manage.py migrate

# Message de fin
echo ""
echo "[6/6] Installation terminée avec succès !"
echo ""
echo "==================================="
echo "Prochaines étapes :"
echo "==================================="
echo "1. Créer un superutilisateur :"
echo "   python manage.py createsuperuser"
echo ""
echo "2. Lancer le serveur :"
echo "   python manage.py runserver"
echo ""
echo "3. Accéder au site :"
echo "   http://localhost:8000"
echo ""
echo "4. Accéder à l'admin :"
echo "   http://localhost:8000/admin"
echo "==================================="
echo ""
