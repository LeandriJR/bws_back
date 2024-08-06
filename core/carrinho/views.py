from django.http import JsonResponse
from rest_framework.views import APIView
import BO.carrinho.carrinho


class AtualizarView(APIView):
    def get(self, request):
        response = BO.carrinho.carrinho.Carrinho().get_carrinho(
            cliente_id=3
        )

        return JsonResponse(response, safe=False, status=response['status_code'])

    def post(self, request):
        response = BO.carrinho.carrinho.Carrinho().alterar_itens_carrinho(
            item_id=self.request.POST.get("item_id"),
            adicionar=True if self.request.POST.get('adicionar') == 'true' else False,
            cliente_id=3
        )
        return JsonResponse(response, safe=False, status=response['status_code'])

    def delete(self, request):
        return JsonResponse({'status': True, 'descricao': 'A implementar', 'status_code': 200})


class AdicionarProdutoView(APIView):

    def post(self, request):
        response = BO.carrinho.carrinho.Carrinho().adicionar_produto_carrinho(
            produto_id=self.request.POST.get("produto_id"),
            cliente_id=3
        )
        return JsonResponse(response, safe=False, status=response['status_code'])