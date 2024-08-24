from BO.sql.conexao import SQLConexao
from core.decorators import Response


class Funcionario(SQLConexao):
    def __init__(self):
        super().__init__()

    @Response(desc_success="Sucesso ao Logar",
              desc_error='Erro ao Logar',
              lista_retornos=['token', 'nm_completo', 'pagina_inicial'])
    def buscar_informacao(self, user=None):
        return user['token'], self.buscar_nome_funcionario(username=user['user'].username), 'home'

    @Response(is_manter_retorno=True)
    def buscar_nome_funcionario(self, username=None):
        return self.select(query=f"""
                        SELECT initcap(nm_completo)
                        FROM {self.schema_cliente}.cliente
                        WHERE user_id = :cpf """
                           , parametros={'cpf': username}
                           , is_primeiro=True
                           , is_values_list=True)

