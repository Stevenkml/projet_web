@echo off
echo ===================================
echo Installation de LocaFrance Django
echo ===================================
echo.

:: Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR : Python n'est pas installé !
    echo Téléchargez Python sur https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/6] Python détecté !
echo.

:: Créer l'environnement virtuel
echo [2/6] Création de l'environnement virtuel...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERREUR : Impossible de créer l'environnement virtuel
    pause
    exit /b 1
)

:: Activer l'environnement virtuel
echo [3/6] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

:: Installer les dépendances
echo [4/6] Installation des dépendances...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERREUR : Installation des dépendances échouée
    pause
    exit /b 1
)

:: Créer la base de données
echo [5/6] Configuration de la base de données...
python manage.py makemigrations
python manage.py migrate

:: Message de fin
echo.
echo [6/6] Installation terminée avec succès !
echo.
echo ===================================
echo Prochaines étapes :
echo ===================================
echo 1. Créer un superutilisateur :
echo    python manage.py createsuperuser
echo.
echo 2. Lancer le serveur :
echo    python manage.py runserver
echo.
echo 3. Accéder au site :
echo    http://localhost:8000
echo.
echo 4. Accéder à l'admin :
echo    http://localhost:8000/admin
echo ===================================
echo.
pause
