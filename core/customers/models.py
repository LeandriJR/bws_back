from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from core.models import Log


# Create your models here.
class Conta(Log, TenantMixin):
    nome = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=512, null=True)

    class Meta:
        db_table = u'conta'


class Dominio(DomainMixin):

    class Meta:
        db_table = u'conta_dominio'


class ConfiguracaoPadrao(Log):
    app_menu = models.JSONField(null=True)
    site_menu = models.JSONField(null=True)
    app_configuracao = models.JSONField(null=True)
    site_configuracao = models.JSONField(null=True)

    class Meta:
        db_table = u'conta_configuracaopadrao'