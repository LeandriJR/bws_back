from django.db import models

# Create your models here.
from django.db import models
import core.models


class Cliente(core.models.Log, core.models.PessoaLog):
    user = models.OneToOneField('usuario.User', on_delete=models.DO_NOTHING, null=True)

    endereco = models.ForeignKey('core.Endereco', on_delete=models.DO_NOTHING, null=True, related_name='endereco')

    class Meta:
        db_table = 'cliente'
