from django.urls import path
from .views import (
    mes_conversations,
    conversation_avec_user,
    envoyer_message,
    messages_non_lus
)

app_name = 'messages_app'

urlpatterns = [
    path('mes-conversations/', mes_conversations, name='mes-conversations'),
    path('conversation/<int:user_id>/', conversation_avec_user, name='conversation'),
    path('', envoyer_message, name='envoyer'),
    path('non-lus/', messages_non_lus, name='non-lus'),
]