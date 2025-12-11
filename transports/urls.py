from django.urls import path
from .views import rechercher_trajets, liste_villes

app_name = 'transports'

urlpatterns = [
    path('trajets/', rechercher_trajets, name='trajets'),
    path('villes/', liste_villes, name='villes'),
]