# Generated by Django 5.0.6 on 2024-06-08 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_configuracaopadrao_delete_configuracao'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracaopadrao',
            name='usr_delete',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='configuracaopadrao',
            name='usr_edicao',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='configuracaopadrao',
            name='usr_insercao',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='conta',
            name='usr_delete',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='conta',
            name='usr_edicao',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='conta',
            name='usr_insercao',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
