from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from .models import Logement, Avis
from .serializers import LogementSerializer, AvisSerializer


class LogementListView(generics.ListAPIView):
    """Liste de tous les logements avec filtres"""
    serializer_class = LogementSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Logement.objects.filter(actif=True)
        
        # Filtres
        ville = self.request.query_params.get('ville', None)
        type_logement = self.request.query_params.get('type', None)
        prix_max = self.request.query_params.get('prix_max', None)
        capacite = self.request.query_params.get('capacite', None)
        
        if ville:
            queryset = queryset.filter(ville__icontains=ville)
        
        if type_logement:
            queryset = queryset.filter(type=type_logement)
        
        if prix_max:
            queryset = queryset.filter(prix_par_nuit__lte=prix_max)
        
        if capacite:
            queryset = queryset.filter(capacite_max__gte=capacite)
        
        return queryset.order_by('-created_at')


class LogementDetailView(generics.RetrieveAPIView):
    """Détails d'un logement"""
    queryset = Logement.objects.filter(actif=True)
    serializer_class = LogementSerializer
    permission_classes = [permissions.AllowAny]


class LogementCreateView(generics.CreateAPIView):
    """Créer un logement (hôte uniquement)"""
    serializer_class = LogementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        if self.request.user.role != 'hote':
            raise permissions.PermissionDenied("Seuls les hôtes peuvent créer des logements")
        serializer.save(hote=self.request.user)


class LogementUpdateView(generics.UpdateAPIView):
    """Modifier un logement (hôte propriétaire uniquement)"""
    serializer_class = LogementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Logement.objects.filter(hote=self.request.user)


class LogementDeleteView(generics.DestroyAPIView):
    """Supprimer un logement (hôte propriétaire uniquement)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Logement.objects.filter(hote=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mes_logements(request):
    """Logements de l'hôte connecté"""
    if request.user.role != 'hote':
        return Response(
            {'error': 'Accès réservé aux hôtes'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    logements = Logement.objects.filter(hote=request.user)
    serializer = LogementSerializer(logements, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def logement_avis(request, pk):
    """Avis d'un logement"""
    try:
        logement = Logement.objects.get(pk=pk)
        avis = Avis.objects.filter(logement=logement).order_by('-created_at')
        serializer = AvisSerializer(avis, many=True)
        return Response(serializer.data)
    except Logement.DoesNotExist:
        return Response(
            {'error': 'Logement non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
