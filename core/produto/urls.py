from django.urls import re_path

import core.produto.views
urlpatterns = [
    re_path('categoria', core.produto.views.CategoriaView.as_view(), name='categoria'),
    re_path('produto', core.produto.views.ProdutoView.as_view(), name='produto')
]