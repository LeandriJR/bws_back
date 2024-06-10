from BO.sql.conexao import SQLConexao
from datetime import datetime


class Cliente(SQLConexao):
    def __init__(self):
        super().__init__()

    def criar_cliente_login(self, nm_primeiro=None, nm_ultimo=None, cpf=None, email=None):
        cliente = {
            'user_id': cpf,
            'nm_primeiro': nm_primeiro,
            'nm_ultimo': nm_ultimo,
            'nm_completo': f"{nm_primeiro} {nm_ultimo}",
            'email': email,
            'cpf': cpf,
            'cpf_form': self.formatar_cpf(cpf=cpf),
            'status': True,
            'dat_insercao': datetime.now()
        }

        self.insert(
            nm_tabela='cliente',
            dict_coluna_valor=cliente,
            is_primeiro=False

        )

        return True

    def formatar_cpf(self, cpf=None):
        cpf = ''.join(filter(str.isdigit, cpf))

        if len(cpf) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos.")

        cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf_formatado

    def buscar_username_login(self, email=None):
        return self.select(query=f"""
            SELECT username FROM {self.schema_cliente}.user
            WHERE email = :email
        """,
        parametros={'email': email},
        is_values_list=True,
        is_primeiro=True)

    def buscar_login_existente(self, email=None, cpf=None):
        return self.select(query=f"""
                    SELECT username FROM {self.schema_cliente}.user
                    WHERE email = :email or username = :cpf
                """,
                           parametros={'email': email, 'cpf': cpf},
                           is_values_list=True,
                           is_primeiro=True)

