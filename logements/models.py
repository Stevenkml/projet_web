from django.db import models
from django.conf import settings


class Logement(models.Model):
    """Modèle pour les logements"""
    
    TYPE_CHOICES = [
        ('appartement', 'Appartement'),
        ('maison', 'Maison'),
        ('studio', 'Studio'),
        ('villa', 'Villa'),
        ('chambre', 'Chambre'),
    ]
    
    hote = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='logements',
        limit_choices_to={'role': 'hote'}
    )
    
    titre = models.CharField(max_length=200, verbose_name='Titre')
    description = models.TextField(verbose_name='Description')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Type')
    
    adresse = models.CharField(max_length=255, verbose_name='Adresse')
    ville = models.CharField(max_length=100, verbose_name='Ville')
    code_postal = models.CharField(max_length=10, verbose_name='Code postal')
    
    prix_par_nuit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Prix par nuit')
    capacite_max = models.IntegerField(verbose_name='Capacité maximum')
    nombre_chambres = models.IntegerField(default=1, verbose_name='Nombre de chambres')
    nombre_salles_bain = models.IntegerField(default=1, verbose_name='Nombre de salles de bain')
    
    photo_url = models.URLField(blank=True, null=True, verbose_name='URL de la photo')
    
    wifi = models.BooleanField(default=False, verbose_name='WiFi')
    parking = models.BooleanField(default=False, verbose_name='Parking')
    cuisine = models.BooleanField(default=False, verbose_name='Cuisine')
    animaux = models.BooleanField(default=False, verbose_name='Animaux acceptés')
    
    actif = models.BooleanField(default=True, verbose_name='Actif')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Dernière modification')
    
    class Meta:
        verbose_name = 'Logement'
        verbose_name_plural = 'Logements'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.titre} - {self.ville}"
    
    @property
    def note_moyenne(self):
        """Calcule la note moyenne des avis"""
        avis = self.avis.all()
        if avis.exists():
            return round(sum(a.note for a in avis) / avis.count(), 1)
        return None
    
    @property
    def nombre_avis(self):
        """Retourne le nombre d'avis"""
        return self.avis.count()


class Avis(models.Model):
    """Modèle pour les avis sur les logements"""
    
    logement = models.ForeignKey(
        Logement,
        on_delete=models.CASCADE,
        related_name='avis'
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='avis'
    )
    reservation = models.OneToOneField(
        'reservations.Reservation',
        on_delete=models.CASCADE,
        related_name='avis'
    )
    
    note = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Note')
    commentaire = models.TextField(verbose_name='Commentaire')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de publication')
    
    class Meta:
        verbose_name = 'Avis'
        verbose_name_plural = 'Avis'
        ordering = ['-created_at']
        unique_together = ['reservation']
    
    def __str__(self):
        return f"Avis de {self.client.get_full_name()} sur {self.logement.titre} - {self.note}/5"
