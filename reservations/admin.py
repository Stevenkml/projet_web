from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'logement', 'client', 'date_debut', 'date_fin', 'nombre_voyageurs', 'prix_total', 'statut', 'created_at']
    list_filter = ['statut', 'date_debut', 'created_at']
    search_fields = ['logement__titre', 'client__email']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Réservation', {
            'fields': ('logement', 'client', 'statut')
        }),
        ('Dates', {
            'fields': ('date_debut', 'date_fin')
        }),
        ('Détails', {
            'fields': ('nombre_voyageurs', 'prix_total', 'message')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
