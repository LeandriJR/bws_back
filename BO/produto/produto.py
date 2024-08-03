import http

from BO.sql.conexao import SQLConexao


class Produto(SQLConexao):
    def __init__(self):
        super().__init__()

    def buscar_produtos_por_categoria(self, categoria_id=None):
        try:
            produtos = self.select(query=f"""
                                SELECT        p.id
                                            , p.nome       					as descricao
                                            , p.imagem
                                            , p.descricao  					as ingredientes
                                            , p.tamanho
                                            , pc.nome
                                            , pc.id 						as categoria_id
                                            , pc.nome 						as categoria
                                            , pp.valor 	  					as preco
                                            , pd.valor_final 				as preco_desconto 
                                            , pt.nome 		 				as tipo_desconto
                                    FROM {self.schema_cliente}.produtos p
                                    INNER JOIN {self.schema_cliente}.produto_categoria pc ON pc.id = p.categoria_id
                                    INNER JOIN {self.schema_cliente}.produto_preco pp ON p.id = pp.produto_id
                                    LEFT JOIN {self.schema_cliente}.produto_desconto pd ON pp.desconto_id = pd.id
                                    LEFT JOIN {self.schema_cliente}.produto_tipodesconto pt on pt.nome = pd.tipo_id 
                                    WHERE p.status = true
                                          AND categoria_id = :categoria_id
                                          AND (pd.status or pd.status is null)
                                    ORDER BY p.ordem
                            """,
                            parametros={'categoria_id': categoria_id})
            return {
                'status': True,
                'status_code': http.HTTPStatus.OK if produtos else http.HTTPStatus.NOT_FOUND,
                'produtos': produtos,
                'descricao': 'Sucesso ao buscar produtos' if produtos else 'Nenhum produto encontrado!'
            }

        except:
            return {
                'status': False,
                'status_code': http.HTTPStatus.INTERNAL_SERVER_ERROR,
                'descricao': "Erro ao buscar produtos"
            }
