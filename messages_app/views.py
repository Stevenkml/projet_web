from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Max, Count, Case, When, IntegerField
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mes_conversations(request):
    """
    Liste des conversations de l'utilisateur connecté avec nombre de messages non lus
    """
    user = request.user
    
    # Trouver tous les utilisateurs avec qui on a échangé
    conversations_ids = Message.objects.filter(
        Q(expediteur=user) | Q(destinataire=user)
    ).values_list('expediteur_id', 'destinataire_id')
    
    # Extraire les IDs uniques (sans l'utilisateur actuel)
    user_ids = set()
    for exp_id, dest_id in conversations_ids:
        if exp_id != user.id:
            user_ids.add(exp_id)
        if dest_id != user.id:
            user_ids.add(dest_id)
    
    conversations = []
    
    for user_id in user_ids:
        other_user = User.objects.get(id=user_id)
        
        # Dernier message de la conversation
        dernier_message = Message.objects.filter(
            Q(expediteur=user, destinataire=other_user) |
            Q(expediteur=other_user, destinataire=user)
        ).order_by('-created_at').first()
        
        # Nombre de messages non lus
        non_lus = Message.objects.filter(
            expediteur=other_user,
            destinataire=user,
            lu=False
        ).count()
        
        conversations.append({
            'user_id': other_user.id,
            'prenom': other_user.prenom,
            'nom': other_user.nom,
            'email': other_user.email,
            'role': other_user.role,
            'dernier_message': dernier_message.contenu if dernier_message else None,
            'derniere_date': dernier_message.created_at if dernier_message else None,
            'non_lus': non_lus
        })
    
    # Trier par date du dernier message
    conversations.sort(key=lambda x: x['derniere_date'] if x['derniere_date'] else '', reverse=True)
    
    return Response(conversations)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversation_avec_user(request, user_id):
    """
    Récupérer tous les messages d'une conversation avec un utilisateur spécifique
    """
    user = request.user
    
    try:
        other_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    
    # Récupérer tous les messages entre les deux utilisateurs
    messages = Message.objects.filter(
        Q(expediteur=user, destinataire=other_user) |
        Q(expediteur=other_user, destinataire=user)
    ).order_by('created_at')
    
    # Marquer les messages reçus comme lus
    Message.objects.filter(
        expediteur=other_user,
        destinataire=user,
        lu=False
    ).update(lu=True)
    
    messages_data = [{
        'id': msg.id,
        'expediteur_id': msg.expediteur.id,
        'expediteur_nom': f"{msg.expediteur.prenom} {msg.expediteur.nom}",
        'destinataire_id': msg.destinataire.id,
        'contenu': msg.contenu,
        'lu': msg.lu,
        'created_at': msg.created_at
    } for msg in messages]
    
    return Response(messages_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def envoyer_message(request):
    """
    Envoyer un message à un utilisateur
    """
    user = request.user
    destinataire_id = request.data.get('destinataire_id')
    contenu = request.data.get('contenu')
    
    if not destinataire_id or not contenu:
        return Response(
            {'error': 'Destinataire et contenu requis'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        destinataire = User.objects.get(id=destinataire_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'Destinataire non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Créer le message
    message = Message.objects.create(
        expediteur=user,
        destinataire=destinataire,
        contenu=contenu
    )
    
    return Response({
        'id': message.id,
        'expediteur_id': message.expediteur.id,
        'destinataire_id': message.destinataire.id,
        'contenu': message.contenu,
        'created_at': message.created_at
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def messages_non_lus(request):
    """
    Nombre total de messages non lus
    """
    count = Message.objects.filter(
        destinataire=request.user,
        lu=False
    ).count()
    
    return Response({'non_lus': count})