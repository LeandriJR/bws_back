from django.db import models

# Create your models here.
from django.db import models
from core.models import Log, PessoaLog, EnderecoMeta


class Cliente(Log, PessoaLog):
    user = models.OneToOneField('usuario.User', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'app_cliente'


class Endereco(EnderecoMeta, Log):
    cliente = models.ForeignKey('Cliente', on_delete=models.DO_NOTHING, null=True, related_name='app_cliente')
    is_principal = models.BooleanField(null=True, default=True)

    class Meta:
        db_table = 'cliente_endereco'
