from django.urls import re_path, include
import core.usuario.cliente.urls
urlpatterns = [
    re_path('cliente', include(core.usuario.cliente.urls))
]