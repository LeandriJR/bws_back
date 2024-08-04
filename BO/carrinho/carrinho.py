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
            parametros={'cliente_id': cliente_id})

            return {
                'status': True,
                'descricao': 'Sucesso ao buscar carrinho' if carrinho else "Nenhum carrinho encontrado",
                'data': carrinho if carrinho else [],
                'status_code': http.HTTPStatus.OK
            }
        except:
            return {
                'status': True,
                'descricao': 'Erro ao buscar carrinho',
                'data': [],
                'status_code': http.HTTPStatus.INTERNAL_SERVER_ERROR
            }