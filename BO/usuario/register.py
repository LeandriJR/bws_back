from BO.sql.conexao import SQLConexao
import core.usuario.models
import BO.usuario.cliente


class Register(SQLConexao):
    def __init__(self):
        super().__init__()

    def registrar(self, response=None):
        try:
            username = BO.usuario.cliente.Cliente().buscar_login_existente(response['email'], response['cpf'])
            if username:
                return {  'status': False,
                          'descricao': 'Email ou CPF de usuário já cadastrado!',
                          'data': {},
                          'status_code': 403
                  }
            core.usuario.models.User.objects.create_user(username=response['cpf'],
                                                         email=response['email'],
                                                         password=response['password'],
                                                         nm_primeiro=response['nm_primeiro'],
                                                         nm_ultimo=response['nm_ultimo'])

            BO.usuario.cliente.Cliente().criar_cliente_login(
                cpf=response['cpf'],
                email=response['email'],
                nm_primeiro=response['nm_primeiro'],
                nm_ultimo=response['nm_ultimo']
            )

            return {'status': True,
                      'descricao': 'Registrado com sucesso!',
                      'data': {},
                      'status_code': 200
                  }
        except:
            return {'status': False,
                    'descricao': 'Erro ao tentar registrar usuario',
                    'data': {},
                    'status_code': 501
                    }