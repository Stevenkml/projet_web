from rest_framework import serializers
from .models import Logement, Avis
from django.contrib.auth import get_user_model

User = get_user_model()


class LogementSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les logements"""
    note_moyenne = serializers.ReadOnlyField()
    nombre_avis = serializers.ReadOnlyField()
    hote_nom = serializers.SerializerMethodField()
    
    class Meta:
        model = Logement
        fields = [
            'id', 'titre', 'description', 'type', 'adresse', 'ville', 
            'code_postal', 'prix_par_nuit', 'capacite_max', 'nombre_chambres',
            'nombre_salles_bain', 'photo_url', 'wifi', 'parking', 'cuisine',
            'animaux', 'actif', 'created_at', 'note_moyenne', 'nombre_avis',
            'hote_nom', 'hote'
        ]
        read_only_fields = ['id', 'created_at', 'hote']
    
    def get_hote_nom(self, obj):
        return f"{obj.hote.prenom} {obj.hote.nom}"


class AvisSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les avis"""
    client_nom = serializers.SerializerMethodField()
    client_prenom = serializers.SerializerMethodField()
    
    class Meta:
        model = Avis
        fields = ['id', 'note', 'commentaire', 'created_at', 'client_nom', 'client_prenom']
        read_only_fields = ['id', 'created_at', 'client']
    
    def get_client_nom(self, obj):
        return obj.client.nom
    
    def get_client_prenom(self, obj):
        return obj.client.prenom
