from django.urls import path
from .views import (
    LogementListView,
    LogementDetailView,
    LogementCreateView,
    LogementUpdateView,
    LogementDeleteView,
    mes_logements,
    logement_avis
)

app_name = 'logements'

urlpatterns = [
    path('', LogementListView.as_view(), name='list'),
    path('<int:pk>/', LogementDetailView.as_view(), name='detail'),
    path('create/', LogementCreateView.as_view(), name='create'),
    path('<int:pk>/update/', LogementUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', LogementDeleteView.as_view(), name='delete'),
    path('hote/mes-logements/', mes_logements, name='mes-logements'),
    path('<int:pk>/avis/', logement_avis, name='avis'),
]
