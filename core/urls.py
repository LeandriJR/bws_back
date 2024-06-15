from django.urls import re_path, include
import core.usuario.urls
import core.produto.urls
import core.views
urlpatterns = [
    re_path('usuario', include(core.usuario.urls), name='usuario'),
    re_path('produto', include(core.produto.urls), name='produto'),
    re_path('status_api', core.views.StatusAPIView.as_view(), name='status_api'),
]
