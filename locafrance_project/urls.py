from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Routes
    path('api/auth/', include('accounts.urls')),
    path('api/logements/', include('logements.urls')),
    path('api/reservations/', include('reservations.urls')),
    path('api/messages/', include('messages_app.urls')),
    path('api/transports/', include('transports.urls')),
    
    # Pages frontend
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('pages/client-dashboard.html', TemplateView.as_view(template_name='pages/client-dashboard.html'), name='client-dashboard'),
    path('pages/logement-details.html', TemplateView.as_view(template_name='pages/logement-details.html'), name='logement-details'),
    path('pages/hote-dashboard.html', TemplateView.as_view(template_name='pages/hote-dashboard.html'), name='hote-dashboard'),
    path('pages/messagerie.html', TemplateView.as_view(template_name='pages/messagerie.html'), name='messagerie'),
]

# Servir les fichiers médias et statiques en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)