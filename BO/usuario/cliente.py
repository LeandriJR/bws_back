from BO.sql.conexao import SQLConexao
from datetime import datetime

from core.decorators import Response


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

    def buscar_informacao(self, username=None):
        return {
            'nome_completo': self.buscar_nome_cliente(username=username),
        }

    def buscar_nome_cliente(self, username=None):
        return self.select(query=f"""
                SELECT initcap(nm_completo)
                FROM {self.schema_cliente}.cliente
                WHERE user_id = :cpf """
            ,parametros={'cpf': username}
            ,is_primeiro=True
            ,is_values_list=True)

    @Response(desc_success="Sucesso ao buscar endereço",
              desc_error="Erro ao buscar endereço",
              lista_retornos=['lista_endereco'])
    def buscar_endereco_cliente(self, user_id=None):
        return self.select(query=f"""
                        SELECT    ce.id
                                , ce.endereco_completo
                                , ce.cep
                                , ce.rua
                                , ce.numero
                                , ce.complemento
                                , ce.bairro
                                , ce.cidade
                                , ce.ponto_referencia
                                , ce.latitude
                                , ce.longitude
                                , pce.nm_descritivo as estado
                                , pce.regiao_codigo as estado_sigla
                                , ce.is_principal
                        FROM {self.schema_cliente}.cliente_endereco ce
                        left JOIN public.core_estado pce ON ce.estado_id = pce.estado
                        WHERE ce.cliente_id  = :cliente_id and ce.status
                        ORDER BY ce.is_principal DESC, ce.dat_insercao
                        """,
                   parametros={'cliente_id': user_id})

    @Response(desc_success="Sucesso ao salvar endereço",
              desc_error="Erro ao salvar endereço",
              lista_retornos=['lista_endereco'])
    def salvar_endereco_usuario(self, user_id=None, endereco_id=None, cep=None, rua=None, numero=None, complemento=None, bairro=None,
                                cidade=None, ponto_referencia=None, latitude=None, longitude=None, estado_id=None,
                                estado_sigla=None, is_principal=None):

        endereco = {
            'endereco_completo': f'{rua}, {numero}, {bairro} - {cidade}-{estado_sigla}',
            'cliente_id': user_id,
            'cep': cep,
            'rua': rua,
            'numero': numero,
            'complemento': complemento,
            'bairro': bairro,
            'cidade': cidade,
            'ponto_referencia': ponto_referencia,
            'latitude': latitude,
            'longitude': longitude,
            'estado_id': estado_id,
            'is_principal': is_principal
        }
        if not endereco_id:
            self.insert(nm_tabela='cliente_endereco',
                        dict_coluna_valor=endereco,
                        is_primeiro=False)
        else:
            if endereco['is_principal']:
                self.update(nm_tabela='cliente_endereco',
                        dict_coluna_valor={'is_principal': False},
                        filtro_where={'cliente_id': user_id},
                        is_primeiro=False)

            self.update(nm_tabela='cliente_endereco',
                        dict_coluna_valor=endereco,
                        filtro_where={'id': endereco_id},
                        is_primeiro=False)

        return self.buscar_endereco_cliente(user_id=user_id).get('data').get('lista_endereco')

    @Response(desc_success="Sucesso ao mudar status do endereço",
              desc_error="Erro ao mudar status do endereço",
              lista_retornos=['lista_endereco'])
    def trocar_status_endereco_cliente(self, user_id, endereco_id=None):
        self.update(nm_tabela='cliente_endereco',
                    dict_coluna_valor={'status': False},
                    filtro_where={'cliente_id': user_id, 'id': endereco_id},
                    is_primeiro=False)

        return self.buscar_endereco_cliente(user_id=user_id).get('data').get('lista_endereco')