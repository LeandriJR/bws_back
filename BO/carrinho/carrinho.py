import http

from BO.sql.conexao import SQLConexao
from core.decorators import Response


class Carrinho(SQLConexao):
    def __init__(self):
        super().__init__()

    @Response(desc_success="Sucesso ao buscar carrinho",
              desc_error='Erro ao buscar carrinho',
              lista_retornos=['carrinho'])
    def get_carrinho(self, cliente_id=None):
        carrinho = self.select(query=f"""
                   SELECT cc.id,
                          COALESCE(
                              (
                                  SELECT json_agg(
                                             json_build_object(
                                                 'id', cci.id::bigint,
                                                 'descricao', p.nome,
                                                 'preco', pp.valor::float,
                                                 'quantidade', cci.quantidade::int,
                                                 'imagem', p.imagem
                                             )
                                         )
                                  FROM develop.cliente_carrinhoitem cci
                                  LEFT JOIN develop.produtos p ON p.id = cci.produto_id
                                  LEFT JOIN develop.produto_preco pp ON pp.produto_id = p.id
                                  WHERE cci.carrinho_id = cc.id and cci.quantidade > 0
                              ),
                              '[]'::json
                          ) AS itens,
                          sum(pp.valor * cci.quantidade)::float as preco_total
                   FROM develop.cliente_carrinho cc
                   left join develop.cliente_carrinhoitem cci on cci.carrinho_id = cc.id
                   LEFT JOIN develop.produtos p ON p.id = cci.produto_id
                   LEFT JOIN develop.produto_preco pp ON pp.produto_id = p.id
                   WHERE cliente_id = :cliente_id
                   group by cc.id
               """,
               parametros={'cliente_id': cliente_id},
               is_primeiro=True)

        return carrinho

    @Response(desc_success="Sucesso ao alterar quantidade de itens",
              desc_error='Erro ao alterar quantidade de itens',
              lista_retornos=['carrinho'])
    def alterar_itens_carrinho(self, item_id=None, adicionar=None, cliente_id=6):
        quantidade = self.select(query=f"""
            select quantidade
            from {self.schema_cliente}.cliente_carrinhoitem
            where id = :item_id
        """,
        parametros={'item_id': int(item_id)},
        is_values_list=True,
        is_primeiro=True) or 0

        if adicionar:
            quantidade = int(quantidade) + 1
        else:
            quantidade = int(quantidade) - 1 if quantidade > 0 else 0

        self.update(nm_tabela='cliente_carrinhoitem',
                    dict_coluna_valor={'quantidade': quantidade},
                    filtro_where={'id': item_id})

        return self.get_carrinho(cliente_id=cliente_id).get('data').get('carrinho')

    @Response(desc_success="Sucesso ao adicionar produto no carrinho",
              desc_error='Erro ao adicionar produto no carrinho',
              lista_retornos=['carrinho'])
    def adicionar_produto_carrinho(self, produto_id=None, cliente_id=None):
        carrinho_id = self.select(query=f"""
                        select  cc.id
                        from {self.schema_cliente}.cliente_carrinho cc
                        where cc.cliente_id = :cliente_id
                    """,
                    parametros={'cliente_id': cliente_id},
                    is_primeiro=True,
                    is_values_list=True)

        if not carrinho_id:
            carrinho_id = self.insert(
                nm_tabela='cliente_carrinho',
                dict_coluna_valor={
                    'cliente_id': cliente_id,
                    'origem': 'delivery',
                    'session_key': hash(cliente_id)
                },
                is_primeiro=False
            ).get('id')
        quantidade = self.select(query=f"""
                           SELECT cci.quantidade::int
                           FROM {self.schema_cliente}.cliente_carrinhoitem cci
                           WHERE cci.produto_id = :produto_id and cci.carrinho_id = :carrinho_id
                       """,
                       parametros={'produto_id': produto_id, 'carrinho_id': carrinho_id},
                    is_primeiro=True,
                    is_values_list=True)

        if quantidade != None:
            self.update(
                nm_tabela='cliente_carrinhoitem',
                dict_coluna_valor={'quantidade': int(quantidade) + 1},
                filtro_where={'produto_id': produto_id, 'carrinho_id': carrinho_id}
            )
        else:
            produto = self.select(query=f"""
                select  pp.id as preco_id,
                        pp.desconto_id as desconto_id
                from {self.schema_cliente}.produtos p
                left join {self.schema_cliente}.produto_preco pp on pp.produto_id = p.id
                where p.id = :produto_id
            """,
            parametros={'produto_id': produto_id},
            is_primeiro=True)

            self.insert(
                nm_tabela='cliente_carrinhoitem',
                dict_coluna_valor={'quantidade': 1,
                                   'status': True,
                                   'carrinho_id': carrinho_id,
                                   'produto_id': produto_id,
                                   'produto_preco_id': produto.get('preco_id'),
                                   'produto_desconto_id': produto.get('desconto_id')}
                , is_primeiro=False)

        return self.get_carrinho(cliente_id=cliente_id).get('data').get('carrinho')

    @Response(desc_success="Sucesso ao adicionar endereco ao carrinho",
              desc_error='Erro ao adicionar endereco ao carrinho',
              lista_retornos=['carrinho'])
    def adicionar_endereco_carrinho(self, endereco_id=None, carrinho_id=None, cliente_id=None):
        self.update(nm_tabela='cliente_carrinho',
                    filtro_where={'id', carrinho_id},
                    dict_coluna_valor={'endereco_id': endereco_id})

        return self.get_carrinho(cliente_id=cliente_id).get('data').get('carrinho')

