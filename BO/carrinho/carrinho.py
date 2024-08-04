from BO.sql.conexao import SQLConexao


class Orcamento(SQLConexao):
    def __init__(self):
        super().__init__()