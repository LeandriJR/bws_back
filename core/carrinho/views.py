from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
import BO.carrinho.carrinho


class CarrinhoView(APIView):
    def get(self, request):
        response = BO.carrinho.carrinho.Carrinho().get_carrinho(
            usuario=self.request.user
        )

        return JsonResponse({'status': True, 'descricao': 'A implementar', 'status_code': 200})

    def post(self, request):
        return JsonResponse({'status': True, 'descricao': 'A implementar', 'status_code': 200})

    def delete(self, request):
        return JsonResponse({'status': True, 'descricao': 'A implementar', 'status_code': 200})