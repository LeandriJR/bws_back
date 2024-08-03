from django.db import models

from BO.produto.categoria import Categoria
from core.models import Log
# Create your models here.
class Produto(Log):

    nome = models.CharField(max_length=200, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    nm_apreviado = models.CharField(max_length=200, null=True)
    imagem_grande = models.FileField(upload_to="produtos", max_length=300, default='produtos/sem-foto.jpg', null=True, blank=True)
    imagem = models.FileField(upload_to="produtos", max_length=300, default='produtos/sem-foto.jpg', null=True, blank=True)
    imagem_media = models.FileField(upload_to="produtos", max_length=300, default='produtos/sem-foto.jpg', null=True, blank=True)
    imagem_pequena = models.FileField(upload_to="produtos", max_length=300, default='produtos/sem-foto.jpg', null=True, blank=True)
    peso = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    qtd_min_venda = models.IntegerField(null=True, blank=True, default=1)
    qtd_max_venda = models.IntegerField(null=True, blank=True)
    qtd_estoque = models.IntegerField(null=True)
    is_visivel = models.BooleanField(null=True)
    is_sem_estoque = models.BooleanField(null=True)
    is_disponivel = models.BooleanField(null=True, default=True)
    is_venda = models.BooleanField(null=True)
    tamanho = models.CharField(max_length=128, null=True)
    categoria = models.ForeignKey("Categoria", on_delete=models.DO_NOTHING, null=True)


    class Meta:
        db_table = u'produtos'


class Categoria(Log):
    nome = models.CharField(max_length=256, null=True)
    descricao = models.CharField(max_length=512, null=True)
    imagem = models.TextField(null=True)
    ordem = models.IntegerField(null=True)
    tags = models.TextField(null=True)
    titulo = models.CharField(max_length=200, null=True)
    url = models.TextField(null=True)
    categoria_pai = models.ForeignKey('Categoria', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = u'produto_categoria'


class ProdutoCategoria(Log):
    produto = models.ForeignKey('Produto', on_delete=models.DO_NOTHING, null=True, blank=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.DO_NOTHING, null=True, blank=True)


    class Meta:
        db_table = u'produto_produtocategoria'


class ProdutoPreco(Log):
    produto = models.ForeignKey('Produto', on_delete=models.DO_NOTHING, null=True, blank=True)
    vlr_padrao = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    valor = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    desconto = models.ForeignKey('Desconto', on_delete=models.DO_NOTHING, null=True)

    dat_ini = models.DateTimeField(null=True)
    dat_fim = models.DateTimeField(null=True)


    class Meta:
        db_table = u'produto_preco'


class TipoDesconto(Log):
    nome = models.CharField(max_length=100, primary_key=True)
    descricao = models.CharField(max_length=200, null=True, blank=True)
    tipo = models.CharField(max_length=10, null=True, blank=True)

    imagem = models.FileField(upload_to="produtos", default='produtos/descontos/default.png', null=True, blank=True)

    cor = models.CharField(max_length=50, null=True)
    cor_hover = models.CharField(max_length=50, null=True)
    is_tempo = models.BooleanField(null=True)
    is_sempre_visivel = models.BooleanField(null=True, default=False)
    configuracoes = models.JSONField(null=True)

    class Meta:
        db_table = u'produto_tipodesconto'


class Desconto(Log):

    tipo = models.ForeignKey('TipoDesconto', on_delete=models.DO_NOTHING, null=True)

    valor_ref = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)  # valor inicial (se nao tiver pega do produto preco)
    valor_desc = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)  # valor de desconto
    valor_final = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)  # valor final (se nao tiver calcula)

    per_desc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    dat_ini = models.DateTimeField(null=True, blank=True)
    dat_fim = models.DateTimeField(null=True, blank=True)
    qtd_limite = models.IntegerField(null=True)

    is_frete_gratis = models.BooleanField(null=True)
    qtd_restante = models.IntegerField(null=True)
    is_loja = models.BooleanField(null=True, default=False)

    class Meta:
        db_table = u'produto_desconto'


class Estoque(Log):
    produto = models.ForeignKey('Produto', on_delete=models.DO_NOTHING, null=True, blank=True)
    quantidade = models.FloatField(null=True, blank=True)
    qtd_real = models.FloatField(null=True, blank=True)
    qtd_reservada = models.IntegerField(null=True)
    is_unidade = models.BooleanField(null=True)
    is_peso = models.BooleanField(null=True)


    #cd_filial = models.ForeignKey('Filial', on_delete=models.DO_NOTHING, null=True, blank=True)


    class Meta:
        db_table = u'produto_estoque'
