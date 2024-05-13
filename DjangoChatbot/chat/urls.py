# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat'  # Namespace

urlpatterns = [
    path('', views.chat_home, name='chat_home'),  # Home page of the chat interface
    path('login/', views.login_view, name='login'),  # Login page
    path('signup/', views.signup_view, name='signup'),  # Signup page
    path('query/', views.query_documents, name='query_documents'),  # Endpoint for document query
]
