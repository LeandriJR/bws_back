from django.db import models
from core.models import Log
from core.customers.models import Conta


class Configuracao(Log):
    app_menu = models.JSONField(null=True)
    site_menu = models.JSONField(null=True)
    app_configuracao = models.JSONField(null=True)
    site_configuracao = models.JSONField(null=True)
    conta = models.ForeignKey(Conta, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = u'conta_configuracao'