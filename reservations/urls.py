from django.urls import path
from .views import (
    ReservationCreateView,
    mes_reservations_client,
    mes_reservations_hote,
    accepter_reservation,
    refuser_reservation,
    annuler_reservation,
    creer_avis
)

app_name = 'reservations'

urlpatterns = [
    path('', ReservationCreateView.as_view(), name='create'),
    path('client/mes-reservations/', mes_reservations_client, name='mes-reservations-client'),
    path('hote/mes-reservations/', mes_reservations_hote, name='mes-reservations-hote'),
    path('<int:pk>/accepter/', accepter_reservation, name='accepter'),
    path('<int:pk>/refuser/', refuser_reservation, name='refuser'),
    path('<int:pk>/annuler/', annuler_reservation, name='annuler'),
    path('<int:pk>/avis/', creer_avis, name='creer-avis'),
]
