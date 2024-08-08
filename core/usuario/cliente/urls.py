from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

import core.usuario.cliente.views
urlpatterns = [
    re_path('login', core.usuario.cliente.views.LoginView.as_view(), name='login'),
    re_path('register', csrf_exempt(core.usuario.cliente.views.RegisterUserView.as_view()), name='registro'),
    re_path('endereco/desativar', core.usuario.cliente.views.EnderecoDesativarView.as_view(), name='endereco/desativar'),
    re_path('endereco', core.usuario.cliente.views.EnderecoView.as_view(), name='endereco')

]