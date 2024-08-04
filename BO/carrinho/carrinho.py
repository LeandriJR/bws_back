from BO.sql.conexao import SQLConexao


class Carrinho(SQLConexao):
    def __init__(self):
        super().__init__()

    def get_carrinho(self, usuario=None):
        return {}