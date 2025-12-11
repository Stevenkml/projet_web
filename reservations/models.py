from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


class Reservation(models.Model):
    """Modèle pour les réservations"""
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('annulee', 'Annulée'),
    ]
    
    logement = models.ForeignKey(
        'logements.Logement',
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations_client',
        limit_choices_to={'role': 'client'}
    )
    
    date_debut = models.DateField(verbose_name='Date de début')
    date_fin = models.DateField(verbose_name='Date de fin')
    nombre_voyageurs = models.IntegerField(verbose_name='Nombre de voyageurs')
    
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Prix total')
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente',
        verbose_name='Statut'
    )
    
    message = models.TextField(blank=True, null=True, verbose_name='Message du client')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Dernière modification')
    
    class Meta:
        verbose_name = 'Réservation'
        verbose_name_plural = 'Réservations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Réservation {self.id} - {self.logement.titre} par {self.client.get_full_name()}"
    
    def clean(self):
        """Validation des dates"""
        if self.date_debut and self.date_fin:
            if self.date_debut >= self.date_fin:
                raise ValidationError("La date de fin doit être après la date de début")
            
            if self.date_debut < timezone.now().date():
                raise ValidationError("La date de début ne peut pas être dans le passé")
            
            # Vérifier les chevauchements avec d'autres réservations
            chevauchements = Reservation.objects.filter(
                logement=self.logement,
                statut='acceptee'
            ).filter(
                models.Q(date_debut__lt=self.date_fin, date_fin__gt=self.date_debut)
            ).exclude(pk=self.pk)
            
            if chevauchements.exists():
                raise ValidationError("Ce logement est déjà réservé pour ces dates")
        
        if self.nombre_voyageurs and self.logement:
            if self.nombre_voyageurs > self.logement.capacite_max:
                raise ValidationError(
                    f"Le nombre de voyageurs dépasse la capacité maximum ({self.logement.capacite_max})"
                )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def nombre_nuits(self):
        """Calcule le nombre de nuits"""
        if self.date_debut and self.date_fin:
            return (self.date_fin - self.date_debut).days
        return 0
    
    @property
    def peut_etre_annulee(self):
        """Vérifie si la réservation peut être annulée"""
        return self.statut in ['en_attente', 'acceptee'] and self.date_debut > timezone.now().date()
