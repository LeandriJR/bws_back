# Generated by Django 5.0.6 on 2024-06-12 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0004_remove_cliente_celular_completo_form_and_more'),
        ('core', '0002_endereco_usr_delete_endereco_usr_edicao_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='endereco',
            name='estado',
        ),
        migrations.DeleteModel(
            name='Tipo',
        ),
        migrations.RemoveField(
            model_name='estado',
            name='regiao_tipo',
        ),
        migrations.DeleteModel(
            name='Endereco',
        ),
    ]
