from django.urls import re_path

import core.carrinho.views

urlpatterns = [
    re_path('atualizar', core.carrinho.views.AtualizarView().as_view(), name='carrinho'),
    re_path('adicionar-produto', core.carrinho.views.AdicionarProdutoView().as_view(), name='adicionar_produto')
]
