from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Reservation
from logements.models import Avis
from .serializers import ReservationSerializer, ReservationCreateSerializer


# ------------------------------
# 🔹 Création d'une réservation
# ------------------------------
class ReservationCreateView(generics.CreateAPIView):
    """Créer une réservation"""
    serializer_class = ReservationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if request.user.role != 'client':
            return Response(
                {'error': 'Seuls les clients peuvent créer des réservations'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservation = serializer.save()
        
        return Response(
            ReservationSerializer(reservation).data,
            status=status.HTTP_201_CREATED
        )


# ------------------------------
# 🔹 Réservations du client
# ------------------------------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mes_reservations_client(request):
    """Réservations du client connecté"""
    if request.user.role != 'client':
        return Response(
            {'error': 'Accès réservé aux clients'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    reservations = Reservation.objects.filter(client=request.user).order_by('-created_at')
    
    data = []
    for reservation in reservations:
        serialized = ReservationSerializer(reservation).data
        serialized['titre'] = reservation.logement.titre
        serialized['ville'] = reservation.logement.ville
        serialized['photo_url'] = reservation.logement.photo_url
        data.append(serialized)
    
    return Response(data)


# ------------------------------
# 🔹 Réservations reçues par un hôte
# ------------------------------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mes_reservations_hote(request):
    """Réservations reçues par l'hôte"""
    if request.user.role != 'hote':
        return Response(
            {'error': 'Accès réservé aux hôtes'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    reservations = Reservation.objects.filter(
        logement__hote=request.user
    ).order_by('-created_at')
    
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)


# ------------------------------
# 🔹 Accepter une réservation
# ------------------------------
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def accepter_reservation(request, pk):
    """Accepter une réservation (hôte uniquement), même si date passée"""
    try:
        reservation = Reservation.objects.get(pk=pk)

        if reservation.logement.hote != request.user:
            return Response(
                {'error': "Vous n'êtes pas le propriétaire de ce logement"},
                status=status.HTTP_403_FORBIDDEN
            )

        if reservation.statut != 'en_attente':
            return Response(
                {'error': 'Cette réservation ne peut plus être modifiée'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.statut = 'acceptee'

        try:
            # On ignore la validation de date pour l'accepter/refuser
            reservation.full_clean(exclude=['date_debut'])
            reservation.save()
        except ValidationError as e:
            return Response(
                {'error': e.message_dict},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    except Reservation.DoesNotExist:
        return Response(
            {'error': 'Réservation non trouvée'},
            status=status.HTTP_404_NOT_FOUND
        )


# ------------------------------
# 🔹 Refuser une réservation
# ------------------------------
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def refuser_reservation(request, pk):
    """Refuser une réservation (hôte uniquement), même si date passée"""
    try:
        reservation = Reservation.objects.get(pk=pk)

        if reservation.logement.hote != request.user:
            return Response(
                {'error': "Vous n'êtes pas le propriétaire de ce logement"},
                status=status.HTTP_403_FORBIDDEN
            )

        if reservation.statut != 'en_attente':
            return Response(
                {'error': 'Cette réservation ne peut plus être modifiée'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.statut = 'refusee'

        # On ignore la validation de date pour le refus
        reservation.full_clean(exclude=['date_debut'])
        reservation.save()

        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    except Reservation.DoesNotExist:
        return Response(
            {'error': 'Réservation non trouvée'},
            status=status.HTTP_404_NOT_FOUND
        )


# ------------------------------
# 🔹 Annuler une réservation
# ------------------------------
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def annuler_reservation(request, pk):
    """Annuler une réservation (client uniquement)"""
    try:
        reservation = Reservation.objects.get(pk=pk)
        
        if reservation.client != request.user:
            return Response(
                {'error': 'Vous ne pouvez annuler que vos propres réservations'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not reservation.peut_etre_annulee:
            return Response(
                {'error': 'Cette réservation ne peut plus être annulée'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservation.statut = 'annulee'
        reservation.save()
        
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)
    
    except Reservation.DoesNotExist:
        return Response(
            {'error': 'Réservation non trouvée'},
            status=status.HTTP_404_NOT_FOUND
        )


# ------------------------------
# 🔹 Créer un avis (COMMENTAIRE FACULTATIF)
# ------------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def creer_avis(request, pk):
    """Créer un avis pour une réservation - Commentaire facultatif"""
    try:
        reservation = Reservation.objects.get(pk=pk)
        
        # Vérification : le client doit être le propriétaire de la réservation
        if reservation.client != request.user:
            return Response(
                {'error': 'Vous ne pouvez noter que vos propres réservations'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Vérification : la réservation doit être acceptée
        if reservation.statut != 'acceptee':
            return Response(
                {'error': "Vous ne pouvez noter qu'une réservation acceptée"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérification : pas d'avis déjà existant
        if hasattr(reservation, 'avis'):
            return Response(
                {'error': 'Vous avez déjà laissé un avis pour cette réservation'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupération des données
        note = request.data.get('note')
        commentaire = request.data.get('commentaire', '').strip()  # ✅ Facultatif
        
        # Validation : la note est OBLIGATOIRE
        if not note:
            return Response(
                {'error': 'La note est obligatoire'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validation : la note doit être entre 1 et 5
        try:
            note = int(note)
            if note < 1 or note > 5:
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                {'error': 'La note doit être un nombre entre 1 et 5'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # ✅ Création de l'avis (commentaire peut être vide)
        avis = Avis.objects.create(
            logement=reservation.logement,
            client=request.user,
            reservation=reservation,
            note=note,
            commentaire=commentaire if commentaire else None  # None si vide
        )
        
        return Response(
            {
                'message': 'Avis publié avec succès',
                'avis_id': avis.id,
                'note': avis.note,
                'commentaire': avis.commentaire
            },
            status=status.HTTP_201_CREATED
        )
    
    except Reservation.DoesNotExist:
        return Response(
            {'error': 'Réservation non trouvée'},
            status=status.HTTP_404_NOT_FOUND
        )