from django.urls import re_path

import core.carrinho.views

urlpatterns = [
    re_path('', core.carrinho.views.CarrinhoView().as_view(), name='carrinho')
]