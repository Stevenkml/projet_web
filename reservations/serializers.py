from rest_framework import serializers
from .models import Reservation
from logements.models import Logement


class ReservationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les réservations"""
    logement_titre = serializers.CharField(source='logement.titre', read_only=True)
    logement_ville = serializers.CharField(source='logement.ville', read_only=True)
    logement_photo = serializers.CharField(source='logement.photo_url', read_only=True)
    client_nom = serializers.CharField(source='client.nom', read_only=True)
    client_prenom = serializers.CharField(source='client.prenom', read_only=True)
    client_email = serializers.CharField(source='client.email', read_only=True)
    nombre_nuits = serializers.ReadOnlyField()
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'logement', 'logement_titre', 'logement_ville', 'logement_photo',
            'client', 'client_nom', 'client_prenom', 'client_email',
            'date_debut', 'date_fin', 'nombre_voyageurs', 'prix_total',
            'statut', 'message', 'created_at', 'nombre_nuits'
        ]
        read_only_fields = ['id', 'client', 'created_at', 'statut']
    
    def validate(self, data):
        """Validation personnalisée"""
        if data['date_debut'] >= data['date_fin']:
            raise serializers.ValidationError("La date de fin doit être après la date de début")
        
        logement = data.get('logement')
        if data['nombre_voyageurs'] > logement.capacite_max:
            raise serializers.ValidationError(
                f"Le nombre de voyageurs dépasse la capacité maximum ({logement.capacite_max})"
            )
        
        return data


class ReservationCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour créer une réservation"""
    logement_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Reservation
        fields = ['logement_id', 'date_debut', 'date_fin', 'nombre_voyageurs', 'prix_total', 'message']
    
    def create(self, validated_data):
        logement_id = validated_data.pop('logement_id')
        try:
            logement = Logement.objects.get(id=logement_id)
        except Logement.DoesNotExist:
            raise serializers.ValidationError("Logement non trouvé")
        
        validated_data['logement'] = logement
        validated_data['client'] = self.context['request'].user
        
        return Reservation.objects.create(**validated_data)
