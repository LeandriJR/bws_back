import http

from BO.sql.conexao import SQLConexao


class Carrinho(SQLConexao):
    def __init__(self):
        super().__init__()

    def get_carrinho(self, cliente_id=None):
        try:
            carrinho = self.select(query=f"""
                SELECT cc.id,
                       COALESCE(
                           (
                               SELECT json_agg(
                                          json_build_object(
                                              'id', cci.id,
                                              'descricao', p.nome,
                                              'preco', pp.valor,
                                              'quantidade', cci.quantidade,
                                              'imagem', p.imagem
                                          )
                                      )
                               FROM develop.cliente_carrinhoitem cci
                               LEFT JOIN develop.produtos p ON p.id = cci.produto_id
                               LEFT JOIN develop.produto_preco pp ON pp.produto_id = p.id
                               WHERE cci.carrinho_id = cc.id
                           ),
                           '[]'::json
                       ) AS itens,
                       sum(pp.valor) as preco_total
                FROM develop.cliente_carrinho cc
                left join develop.cliente_carrinhoitem cci on cci.carrinho_id = cc.id
                LEFT JOIN develop.produtos p ON p.id = cci.produto_id
                LEFT JOIN develop.produto_preco pp ON pp.produto_id = p.id
                WHERE cliente_id = :cliente_id
                group by 1
            """,
            parametros={'cliente_id': cliente_id},
            is_primeiro=True)

            return {
                'status': True,
                'descricao': 'Sucesso ao buscar carrinho' if carrinho else "Nenhum carrinho encontrado",
                'data': {
                    'carrinho': carrinho if carrinho else []
                },
                'status_code': http.HTTPStatus.OK
            }
        except:
            return {
                'status': True,
                'descricao': 'Erro ao buscar carrinho',
                'data': [],
                'status_code': http.HTTPStatus.INTERNAL_SERVER_ERROR
            }

    def alterar_itens_carrinho(self, item_id=None, adicionar=None):
        try:
            quantidade = self.select(query=f"""
                select quantidade
                from {self.schema_cliente}.cliente_carrinhoitem
                where id = :item_id
            """,
            parametros={'item_id': item_id},
            is_values_list=True) or 0

            if adicionar:
                quantidade = int(quantidade) + 1
            else:
                quantidade = int(quantidade) - 1 if quantidade > 0 else 0

            self.update(nm_tabela='cliente_carrinhoitem',
                        dict_coluna_valor={'quantidade': quantidade},
                        filtro_where={'id': item_id})

            return {
                'status': False,
                'descricao': 'Erro ao alterar quantidade de itens',
                'status_code': http.HTTPStatus.OK,
                'data': [
                    {'quantidade': quantidade}
                ]
            }
        except:
            return {
                'status': False,
                'descricao': 'Erro ao alterar quantidade de itens',
                'status_code': http.HTTPStatus.INTERNAL_SERVER_ERROR,
                'data': []
            }
