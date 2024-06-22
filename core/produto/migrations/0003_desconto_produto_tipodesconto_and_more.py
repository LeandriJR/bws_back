# Generated by Django 5.0.6 on 2024-06-16 19:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0002_alter_produtocategoria_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desconto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dat_insercao', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_edicao', models.DateTimeField(auto_now=True, null=True)),
                ('dat_delete', models.DateTimeField(blank=True, null=True)),
                ('usr_insercao', models.IntegerField(blank=True, null=True)),
                ('usr_edicao', models.IntegerField(blank=True, null=True)),
                ('usr_delete', models.IntegerField(blank=True, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('valor_ref', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('valor_desc', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('valor_final', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('per_desc', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('dat_ini', models.DateTimeField(blank=True, null=True)),
                ('dat_fim', models.DateTimeField(blank=True, null=True)),
                ('qtd_limite', models.IntegerField(null=True)),
                ('is_frete_gratis', models.BooleanField(null=True)),
                ('qtd_restante', models.IntegerField(null=True)),
                ('is_loja', models.BooleanField(default=False, null=True)),
            ],
            options={
                'db_table': 'produto_desconto',
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dat_insercao', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_edicao', models.DateTimeField(auto_now=True, null=True)),
                ('dat_delete', models.DateTimeField(blank=True, null=True)),
                ('usr_insercao', models.IntegerField(blank=True, null=True)),
                ('usr_edicao', models.IntegerField(blank=True, null=True)),
                ('usr_delete', models.IntegerField(blank=True, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('nome', models.CharField(blank=True, max_length=200, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('nm_apreviado', models.CharField(max_length=200, null=True)),
                ('imagem_grande', models.FileField(blank=True, default='produtos/sem-foto.jpg', max_length=300, null=True, upload_to='produtos')),
                ('imagem', models.FileField(blank=True, default='produtos/sem-foto.jpg', max_length=300, null=True, upload_to='produtos')),
                ('imagem_media', models.FileField(blank=True, default='produtos/sem-foto.jpg', max_length=300, null=True, upload_to='produtos')),
                ('imagem_pequena', models.FileField(blank=True, default='produtos/sem-foto.jpg', max_length=300, null=True, upload_to='produtos')),
                ('altura', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('largura', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('profundidade', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('peso', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('qtd_min_venda', models.IntegerField(blank=True, default=1, null=True)),
                ('qtd_max_venda', models.IntegerField(blank=True, null=True)),
                ('qtd_estoque', models.IntegerField(null=True)),
                ('is_visivel', models.BooleanField(null=True)),
                ('is_sem_estoque', models.BooleanField(null=True)),
                ('is_disponivel', models.BooleanField(default=True, null=True)),
                ('is_venda', models.BooleanField(null=True)),
            ],
            options={
                'db_table': 'produtos',
            },
        ),
        migrations.CreateModel(
            name='TipoDesconto',
            fields=[
                ('dat_insercao', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_edicao', models.DateTimeField(auto_now=True, null=True)),
                ('dat_delete', models.DateTimeField(blank=True, null=True)),
                ('usr_insercao', models.IntegerField(blank=True, null=True)),
                ('usr_edicao', models.IntegerField(blank=True, null=True)),
                ('usr_delete', models.IntegerField(blank=True, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('nome', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('descricao', models.CharField(blank=True, max_length=200, null=True)),
                ('tipo', models.CharField(blank=True, max_length=10, null=True)),
                ('imagem', models.FileField(blank=True, default='produtos/descontos/default.png', null=True, upload_to='produtos')),
                ('cor', models.CharField(max_length=50, null=True)),
                ('cor_hover', models.CharField(max_length=50, null=True)),
                ('is_tempo', models.BooleanField(null=True)),
                ('is_sempre_visivel', models.BooleanField(default=False, null=True)),
                ('configuracoes', models.JSONField(null=True)),
            ],
            options={
                'db_table': 'produto_tipodesconto',
            },
        ),
        migrations.RemoveField(
            model_name='produtocategoria',
            name='descricao',
        ),
        migrations.RemoveField(
            model_name='produtocategoria',
            name='imagem',
        ),
        migrations.RemoveField(
            model_name='produtocategoria',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='produtocategoria',
            name='ordem',
        ),
        migrations.RemoveField(
            model_name='produtocategoria',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='produtocategoria',
            name='titulo',
        ),
        migrations.RemoveField(
            model_name='produtocategoria',
            name='url',
        ),
        migrations.AlterModelTable(
            name='produtocategoria',
            table='produto_produtocategoria',
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dat_insercao', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_edicao', models.DateTimeField(auto_now=True, null=True)),
                ('dat_delete', models.DateTimeField(blank=True, null=True)),
                ('usr_insercao', models.IntegerField(blank=True, null=True)),
                ('usr_edicao', models.IntegerField(blank=True, null=True)),
                ('usr_delete', models.IntegerField(blank=True, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('nome', models.CharField(max_length=256, null=True)),
                ('descricao', models.CharField(max_length=512, null=True)),
                ('imagem', models.TextField(null=True)),
                ('ordem', models.IntegerField(null=True)),
                ('tags', models.TextField(null=True)),
                ('titulo', models.CharField(max_length=200, null=True)),
                ('url', models.TextField(null=True)),
                ('categoria_pai', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.categoria')),
            ],
            options={
                'db_table': 'produto_categoria',
            },
        ),
        migrations.AddField(
            model_name='produtocategoria',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.categoria'),
        ),
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dat_insercao', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_edicao', models.DateTimeField(auto_now=True, null=True)),
                ('dat_delete', models.DateTimeField(blank=True, null=True)),
                ('usr_insercao', models.IntegerField(blank=True, null=True)),
                ('usr_edicao', models.IntegerField(blank=True, null=True)),
                ('usr_delete', models.IntegerField(blank=True, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('quantidade', models.IntegerField(blank=True, null=True)),
                ('qtd_real', models.IntegerField(blank=True, null=True)),
                ('qtd_reservada', models.IntegerField(null=True)),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.produto')),
            ],
            options={
                'db_table': 'produto_estoque',
            },
        ),
        migrations.AddField(
            model_name='produtocategoria',
            name='produto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.produto'),
        ),
        migrations.CreateModel(
            name='ProdutoPreco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dat_insercao', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_edicao', models.DateTimeField(auto_now=True, null=True)),
                ('dat_delete', models.DateTimeField(blank=True, null=True)),
                ('usr_insercao', models.IntegerField(blank=True, null=True)),
                ('usr_edicao', models.IntegerField(blank=True, null=True)),
                ('usr_delete', models.IntegerField(blank=True, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('vlr_padrao', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('valor', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('dat_ini', models.DateTimeField(null=True)),
                ('dat_fim', models.DateTimeField(null=True)),
                ('desconto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.desconto')),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.produto')),
            ],
            options={
                'db_table': 'produto_preco',
            },
        ),
        migrations.AddField(
            model_name='desconto',
            name='tipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.tipodesconto'),
        ),
    ]
