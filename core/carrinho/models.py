from django.db import models
from core.usuario.cliente.models import Cliente, Endereco
from core.produto.models import Produto, ProdutoPreco, Desconto
from core.models import Log


class Carrinho(Log):
    session_key = models.CharField(max_length=200, null=True)
    cliente = models.OneToOneField(Cliente, on_delete=models.DO_NOTHING, null=True)
    origem = models.CharField(max_length=200, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.DO_NOTHING, null=True)
    #funcionario = models.ForeignKey('funcionario.Funcionario', on_delete=models.DO_NOTHING, null=True) para pedidos em mesa (futuro)
    #cupom = models.ForeignKey('cupom.Cupom', on_delete=models.DO_NOTHING, null=True) (futuro)

    class Meta:
        db_table = "cliente_carrinho"


class CarrinhoItem(Log):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.DO_NOTHING, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING, null=True)
    produto_preco = models.ForeignKey(ProdutoPreco, on_delete=models.DO_NOTHING, null=True)
    produto_desconto = models.ForeignKey(Desconto, on_delete=models.DO_NOTHING, null=True)
    is_entrega = models.BooleanField(null=True)
    valor = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    valor_ini = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    quantidade = models.IntegerField(null=True)
    is_cupom = models.BooleanField(default=False, null=True)

    class Meta:
        db_table = "cliente_carrinhoitem"


#class CarrinhoEntrega(Log):
#    endereco = models.ForeignKey(Endereco, on_delete=models.DO_NOTHING, null=True)
