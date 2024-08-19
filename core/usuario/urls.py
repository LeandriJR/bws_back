from django.urls import re_path, include
import core.usuario.cliente.urls
import core.usuario.funcionario.urls
urlpatterns = [
    re_path('cliente', include(core.usuario.cliente.urls)),
    re_path('funcionario', include(core.usuario.funcionario.urls))
]