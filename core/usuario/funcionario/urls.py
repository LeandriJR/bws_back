from core.usuario.funcionario import views
from django.urls import re_path

urlpatterns = [
    re_path('login', views.LoginView().as_view(), name='login')
]