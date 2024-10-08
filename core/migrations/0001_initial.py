# Generated by Django 5.0.6 on 2024-06-07 23:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('dat_insercao', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_edicao', models.DateTimeField(auto_now=True, null=True)),
                ('dat_delete', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('estado', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('nm_descritivo', models.CharField(max_length=255, null=True)),
                ('regiao_tipo', models.CharField(default='', max_length=255, null=True)),
                ('regiao_codigo', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'core_estado',
            },
        ),
        migrations.CreateModel(
            name='PontoFuncao',
            fields=[
                ('dat_insercao', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_edicao', models.DateTimeField(auto_now=True, null=True)),
                ('dat_delete', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('nome', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('descricao', models.CharField(max_length=512, null=True)),
                ('modulo', models.CharField(max_length=256, null=True)),
            ],
            options={
                'db_table': 'user_pontofuncao',
            },
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dat_insercao', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_edicao', models.DateTimeField(auto_now=True, null=True)),
                ('dat_delete', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('codigo', models.CharField(max_length=200, null=True)),
                ('informacao', models.CharField(max_length=500, null=True)),
                ('tipo', models.CharField(max_length=200, null=True)),
                ('nome', models.CharField(max_length=200, null=True)),
                ('descricao', models.TextField(null=True)),
                ('ordem', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'core_tipo',
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dat_insercao', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_edicao', models.DateTimeField(auto_now=True, null=True)),
                ('dat_delete', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('endereco_completo', models.CharField(max_length=250, null=True)),
                ('cep', models.CharField(max_length=8, null=True)),
                ('numero', models.CharField(max_length=30, null=True)),
                ('complemento', models.CharField(max_length=100, null=True)),
                ('bairro', models.CharField(max_length=100, null=True)),
                ('rua', models.CharField(max_length=100, null=True)),
                ('cidade', models.CharField(max_length=100, null=True)),
                ('ponto_referencia', models.CharField(max_length=100, null=True)),
                ('latitude', models.CharField(max_length=200, null=True)),
                ('longitude', models.CharField(max_length=200, null=True)),
                ('estado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='uf', to='core.estado')),
            ],
            options={
                'db_table': 'core_endereco',
            },
        ),
    ]
