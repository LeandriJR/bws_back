from django.db import models
from core.models import Log
# Create your models here.
class Produto(Log):

    class Meta:
        abstract=True


class ProdutoCategoria(Log):
    nome = models.CharField(max_length=256, null=True)
    descricao = models.CharField(max_length=512, null=True)
    imagem = models.TextField(null=True)
    ordem = models.IntegerField(null=True)
    tags = models.TextField(null=True)
    titulo = models.CharField(max_length=200, null=True)
    url = models.TextField(null=True)

    class Meta:
        db_table = 'produto_categoria'