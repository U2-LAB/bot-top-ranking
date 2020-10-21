from django.urls import path

from .views import ChatView

app_name = 'chats'

urlpatterns = [
    path('chats/', ChatView.as_view())
]
