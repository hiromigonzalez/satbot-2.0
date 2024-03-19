# chat/urls.py
from django.urls import path
from . import views
from .views import chat_home, login_view, signup_view

app_name = 'chat'  # Namespace

urlpatterns = [
    path('', chat_home, name='chat_home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
]
