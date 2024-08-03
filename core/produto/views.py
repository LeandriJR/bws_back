from django.http import JsonResponse
from rest_framework.views import APIView

import BO.produto.categoria
import BO.produto.produto

class CategoriaView(APIView):
    def get(self, request):
        response = BO.produto.categoria.Categoria().buscar_categorias_app()

        return JsonResponse(response, safe=False, status=response['status_code'])


class ProdutoView(APIView):
    def get(self, request):
        response = BO.produto.produto.Produto().buscar_produtos_por_categoria(
            categoria_id=self.request.GET.get('categoria_id')
        )

        return JsonResponse(response, safe=False, status=response['status_code'])
