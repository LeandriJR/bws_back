from django.urls import re_path, include
import core.usuario.urls
urlpatterns = [
    re_path('usuario', include(core.usuario.urls)),
]
