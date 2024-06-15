import http

from BO.sql.conexao import SQLConexao


class Categoria(SQLConexao):
    def __init__(self):
        super().__init__()

    def buscar_categorias_app(self):
        try:
            return {
                'status': True,
                'descricao': '',
                'data': {
                    'categorias': self.get_lista_categorias()
                },
                'status_code': http.HTTPStatus.OK
            }

        except:
            return {
                'status': False,
                'descricao': 'Erro ao buscar categorias',
                'status_code': http.HTTPStatus.INTERNAL_SERVER_ERROR
            }

    def get_lista_categorias(self):
        return self.select(f"""
                                SELECT id, nome, descricao, imagem 
                                FROM {self.schema_cliente}.produto_categoria
                                WHERE status = true
                                ORDER BY ordem 
                        """)