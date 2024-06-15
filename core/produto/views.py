from django.http import JsonResponse
from rest_framework.views import APIView

import BO.produto.categoria


class CategoriaView(APIView):
    def get(self, request):
        response = BO.produto.categoria.Categoria().buscar_categorias_app()

        return JsonResponse(response, safe=False, status=response['status_code'])