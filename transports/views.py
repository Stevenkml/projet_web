from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from urllib.parse import quote


@api_view(['GET'])
@permission_classes([AllowAny])
def rechercher_trajets(request):
    """
    Rechercher des trajets entre deux villes
    """
    try:
        depart = request.query_params.get('depart')
        arrivee = request.query_params.get('arrivee')
        date_aller = request.query_params.get('date_aller', '')
        date_retour = request.query_params.get('date_retour', '')
        
        if not depart or not arrivee:
            return Response(
                {'error': 'Départ et arrivée requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Construction des liens
        lien_rome2rio = f"https://www.rome2rio.com/fr/map/{quote(depart)}/{quote(arrivee)}?departureDate={date_aller}"
        if date_retour:
            lien_rome2rio += f"&returnDate={date_retour}"
        
        lien_google_maps = f"https://www.google.com/maps/dir/{quote(depart)}/{quote(arrivee)}"
        
        lien_trainline = f"https://www.thetrainline.com/fr/train-times/{quote(depart)}-to-{quote(arrivee)}/{date_aller}"
        
        lien_kiwi = f"https://www.kiwi.com/fr/search/results/{quote(depart.lower())}-france/{quote(arrivee.lower())}-france/{date_aller}/{date_retour}"
        
        lien_blablacar = f"https://www.blablacar.fr/search?fn={quote(depart)},+France&tn={quote(arrivee)},+France&db={date_aller}"
        
        return Response({
            'message': 'Comparez les options de transport disponibles',
            'depart': depart,
            'arrivee': arrivee,
            'date_aller': date_aller or 'À définir',
            'liens': {
                'googlemaps': {
                    'nom': 'Google Maps',
                    'description': '🗺️ Itinéraire routier / transports en commun',
                    'url': lien_google_maps
                },
                'rome2rio': {
                    'nom': 'Rome2Rio',
                    'description': '🌍 Comparateur tous moyens de transport',
                    'url': lien_rome2rio
                },
                'kiwi': {
                    'nom': 'Kiwi.com',
                    'description': '✈️ Comparateur vols, trains et bus',
                    'url': lien_kiwi
                },
                'blablacar': {
                    'nom': 'BlaBlaCar',
                    'description': '🚗 Covoiturage entre particuliers',
                    'url': lien_blablacar,
                    'note': f'Recherchez : {depart} → {arrivee}'
                }
            }
        })
        
    except Exception as error:
        print('Erreur:', error)
        return Response(
            {'error': 'Erreur serveur.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def liste_villes(request):
    """
    Liste des villes principales
    """
    villes = [
        'Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice', 'Nantes',
        'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille', 'Rennes',
        'Reims', 'Le Havre', 'Saint-Étienne', 'Toulon', 'Grenoble',
        'Dijon', 'Angers', 'Nîmes', 'Villeurbanne', 'Clermont-Ferrand'
    ]
    
    # Filtrer par recherche si fournie
    recherche = request.query_params.get('recherche', '')
    if recherche:
        villes = [v for v in villes if recherche.lower() in v.lower()]
    
    return Response(villes)