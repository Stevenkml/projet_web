from django.contrib import admin
from .models import Logement, Avis


@admin.register(Logement)
class LogementAdmin(admin.ModelAdmin):
    list_display = ['titre', 'ville', 'type', 'prix_par_nuit', 'capacite_max', 'hote', 'actif', 'created_at']
    list_filter = ['type', 'ville', 'actif', 'wifi', 'parking', 'cuisine', 'animaux']
    search_fields = ['titre', 'ville', 'description']
    list_editable = ['actif']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('hote', 'titre', 'description', 'type', 'actif')
        }),
        ('Localisation', {
            'fields': ('adresse', 'ville', 'code_postal')
        }),
        ('Détails', {
            'fields': ('prix_par_nuit', 'capacite_max', 'nombre_chambres', 'nombre_salles_bain', 'photo_url')
        }),
        ('Équipements', {
            'fields': ('wifi', 'parking', 'cuisine', 'animaux')
        }),
    )


@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ['logement', 'client', 'note', 'created_at']
    list_filter = ['note', 'created_at']
    search_fields = ['logement__titre', 'client__email', 'commentaire']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
