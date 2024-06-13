from django.db import models


# Create your models here.
class DatLog(models.Model):
    dat_insercao = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    dat_edicao = models.DateTimeField(auto_now=True, null=True, blank=True)
    dat_delete = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        abstract = True


class UsrLog(models.Model):
    usr_insercao = models.IntegerField(null=True, blank=True)
    usr_edicao = models.IntegerField(null=True, blank=True)
    usr_delete = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        abstract = True


class Log(DatLog, UsrLog):

    status = models.BooleanField(null=True, default=True)

    class Meta:
        managed = True
        abstract = True


class ContatoLog(models.Model):

    celular_ddd = models.CharField(max_length=3, null=True)
    celular_completo = models.CharField(max_length=50, null=True)

    telefone_ddd = models.CharField(max_length=3, null=True)
    telefone_completo = models.CharField(max_length=50, null=True)

    email = models.EmailField(max_length=200, null=True)

    class Meta(Log.Meta):
        abstract = True


class PessoaLog(ContatoLog):

    nm_completo = models.CharField(max_length=200, null=True)
    nm_primeiro = models.CharField(max_length=200, null=True)
    nm_ultimo = models.CharField(max_length=200, null=True)

    cpf = models.BigIntegerField(null=True)
    cpf_form = models.CharField(max_length=20, null=True)

    rg = models.CharField(max_length=15, null=True)
    rg_form = models.CharField(max_length=15, null=True)

    dat_nasc = models.DateField(null=True)

    imagem = models.TextField(default='fotos/sem-foto.png', null=True)

    nm_mae = models.CharField(max_length=200, null=True)
    nm_pai = models.CharField(max_length=200, null=True)

    class Meta(Log.Meta):
        abstract = True


class EnderecoMeta(models.Model):
    endereco_completo = models.CharField(max_length=250, null=True)

    cep = models.CharField(max_length=8, null=True)
    numero = models.CharField(max_length=30, null=True)
    complemento = models.CharField(max_length=100, null=True)
    bairro = models.CharField(max_length=100, null=True)
    rua = models.CharField(max_length=100, null=True)

    cidade = models.CharField(max_length=100, null=True)
    estado = models.ForeignKey('core.Estado', on_delete=models.DO_NOTHING, related_name='uf', null=True)

    ponto_referencia = models.CharField(max_length=100, null=True)
    latitude = models.CharField(max_length=200, null=True)
    longitude = models.CharField(max_length=200, null=True)

    class Meta:
        abstract = True


class Estado(Log):
    estado = models.CharField(max_length=255, primary_key=True)
    nm_descritivo = models.CharField(max_length=255, null=True)
    regiao_codigo = models.CharField(null=True, max_length=200)


    class Meta:
        db_table = 'core_estado'


class PontoFuncao(Log):
    nome = models.CharField(max_length=256, primary_key=True)
    descricao = models.CharField(max_length=512, null=True)
    modulo = models.CharField(max_length=256, null=True)

    class Meta:
        db_table = u'user_pontofuncao'


