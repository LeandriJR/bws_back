from __future__ import annotations

import re

from sqlalchemy import text
from django.conf import settings
from django.utils import timezone
from core.middleware import get_schema_cliente
from BO.base.excecao import ValidationError


class SQLConexao:
    def __init__(self, request=None, schema=None):
        self.engine = settings.DB_CONNECTIONS['default']['engine']
        self.conexao = settings.DB_CONNECTIONS['default']['conexao']
        self.scoped_session = settings.DB_CONNECTIONS['default']['sessoes']
        self.resultset = []

        if schema:
            self.schema_cliente = schema
        else:
            try:
                self.schema_cliente = get_schema_cliente()
            except:
                self.schema_cliente = ''

        self.request = request

    @staticmethod
    def parse_lista_para_tupla(parametros):
        for p in parametros:
            if isinstance(parametros[p], (list, set)):
                if len(parametros[p]) > 0:
                    parametros[p] = tuple(parametros[p])
                else:
                    parametros[p] = tuple([None])

            elif isinstance(parametros[p], tuple):
                if len(parametros[p]) < 0:
                    parametros[p] = tuple([None])

    def __query(self, query=None, parametros=None, is_serializado=True):
        if parametros is None:
            parametros = {}

        self.parse_lista_para_tupla(parametros)

        with self.engine.begin() as conn:
            texto = text(query)
            self.resultset = conn.execute(texto, parametros)

        if self.resultset.returns_rows:
            return list(self.resultset) if not is_serializado else self.get_dados_serializados()
        else:
            return None

    def select(self, query=None, parametros=None, is_primeiro=False, is_values_list=False, is_serializado=True,
               limite=None, offset=0) -> list | dict | None:
        if 'select *' in query.lower():
            raise ValidationError('Filtre apenas os dados necessários para a busca!')

        if limite:
            query = re.sub(';\\s*$', '', query)
            query = query + f' LIMIT {limite} OFFSET {offset};'

        retorno = self.__query(query=query, is_serializado=is_serializado, parametros=parametros)

        return self.formatar_retorno(retorno=retorno, is_values_list=is_values_list, is_primeiro=is_primeiro)

    @staticmethod
    def formatar_retorno(retorno=None, is_values_list=False, is_primeiro=False) -> any:
        if not retorno:
            return None

        if is_values_list:
            lista_retorno = []
            for linha in retorno:
                values = tuple(linha.values())
                if len(values) == 1:
                    lista_retorno.append(values[0])
                else:
                    lista_retorno.append(values)
            retorno = lista_retorno

        if is_primeiro:
            return retorno[0]

        return retorno

    def get_dados_serializados(self):
        return [row._asdict() for row in self.resultset]

    def __montar_log(self, dict_coluna_valor, is_edicao=False, is_desativar=False):
        dat_agora = timezone.now()

        if is_desativar:
            dict_log = {
                'usr_delete': self.request.user.id if self.request else None,
                'dat_delete': dat_agora,
                # 'origem_delete_codigo': self.request.user.tipo_codigo,
            }

        elif is_edicao:
            dict_log = {
                'usr_edicao': self.request.user.id if self.request else None,
                'dat_edicao': dat_agora,
                # 'origem_edicao_codigo': self.request.user.tipo_codigo,
            }

        else:
            dict_log = {
                'usr_insercao': self.request.user.id if self.request else None,
                'dat_insercao': dat_agora,
                # 'origem_edicao_codigo': self.request.user.tipo_codigo,
                'status': 'true',
            }

        dict_coluna_valor.update(dict_log)

        return dict_coluna_valor

    def insert(self, nm_tabela, dict_coluna_valor, nm_pk='id', is_values_list=False,
               is_primeiro=True):

        if len(nm_tabela.split('.')) == 1:
            nm_tabela = self.schema_cliente + '.' + nm_tabela

        dict_coluna_valor = self.__montar_log(dict_coluna_valor=dict_coluna_valor)

        lista_colunas = dict_coluna_valor.keys()
        colunas = ','.join(lista_colunas)
        nm_valores = ','.join([f':{coluna}' for coluna in lista_colunas])

        query = f'insert into {nm_tabela}({colunas}) values ({nm_valores}) RETURNING {nm_pk};'

        retorno = self.__query(query=query, parametros=dict_coluna_valor)[0]

        return self.formatar_retorno(retorno=retorno, is_values_list=is_values_list, is_primeiro=is_primeiro)

    def update(self, nm_tabela, dict_coluna_valor, filtro_where, nm_pk='id', is_desativar=False, is_values_list=False,
               is_primeiro=True):

        if len(nm_tabela.split('.')) == 1:
            nm_tabela = self.schema_cliente + '.' + nm_tabela

        dict_coluna_valor = self.__montar_log(dict_coluna_valor=dict_coluna_valor, is_edicao=True,
                                              is_desativar=is_desativar)

        lista_colunas = dict_coluna_valor.keys()

        update = ','.join([f'{coluna} = :{coluna}' for coluna in lista_colunas])

        where = ''
        for chave, valor in filtro_where.items():
            if isinstance(valor, list):
                where += f" {chave} in :{chave} and"
            else:
                where += f" {chave} = :{chave} and"

        where = where[:-3]  # Removendo o ultimo 'and'

        query = f'update {nm_tabela} set {update} where {where} returning {nm_pk};'

        dict_coluna_valor.update(filtro_where)

        retorno = self.__query(query=query, parametros=dict_coluna_valor)

        return self.formatar_retorno(retorno=retorno, is_values_list=is_values_list, is_primeiro=is_primeiro)

    def salvar(self, nm_tabela, dict_coluna_valor, nm_pk='id', is_values_list=False,
               is_primeiro=True):

        if len(nm_tabela.split('.')) == 1:
            nm_tabela = self.schema_cliente + '.' + nm_tabela

        is_edicao = nm_pk in dict_coluna_valor

        dict_coluna_valor = self.__montar_log(dict_coluna_valor=dict_coluna_valor, is_edicao=is_edicao)

        lista_colunas = dict_coluna_valor.keys()

        colunas = ','.join(lista_colunas)
        nm_valores = ','.join([f':{coluna}' for coluna in lista_colunas])
        update = ','.join([f'{coluna} = :{coluna}' for coluna in lista_colunas])

        query = f"""
            insert into {nm_tabela}({colunas}) values ({nm_valores}) 
            on conflict ({nm_pk}) do update set {update} RETURNING {nm_pk};
        """

        retorno = self.__query(query=query, parametros=dict_coluna_valor)

        return self.formatar_retorno(retorno=retorno, is_values_list=is_values_list, is_primeiro=is_primeiro)

    def desabilitar(self, nm_tabela, filtro_where, is_values_list=False,
                    is_primeiro=True):

        dict_coluna_valor = {'status': False}

        return self.update(nm_tabela=nm_tabela, dict_coluna_valor=dict_coluna_valor, filtro_where=filtro_where,
                           is_desativar=True, is_values_list=is_values_list, is_primeiro=is_primeiro)

    def bulk_insert(self, nm_tabela, lista_dict_coluna_valor, nm_pk='id',
                    is_values_list=True, is_primeiro=False):
        if len(nm_tabela.split('.')) == 1:
            nm_tabela = self.schema_cliente + '.' + nm_tabela

        colunas = ''
        valores = ''
        parametros = {}
        for contador, dict_coluna_valor in enumerate(lista_dict_coluna_valor):
            dict_coluna_valor = self.__montar_log(dict_coluna_valor=dict_coluna_valor)

            if not colunas:
                colunas = ','.join(dict_coluna_valor.keys())

            nm_valores = ''
            for chave, valor in dict_coluna_valor.items():
                parametros[f"{chave}_{contador}"] = valor
                nm_valores += f" :{chave}_{contador},"
            nm_valores = nm_valores[:-1]  # Removendo a última vírgula

            valores += f"({nm_valores}),"
        valores = valores[:-1]  # Removendo a última vírgula

        query = f'insert into {nm_tabela}({colunas}) values {valores} RETURNING {nm_pk};'

        retorno = self.__query(query=query, parametros=parametros)

        return self.formatar_retorno(retorno=retorno, is_values_list=is_values_list, is_primeiro=is_primeiro)

    def bulk_update(self, nm_tabela, lista_dict_coluna_valor, lista_colunas_atualizar, nm_pk='id',
                    is_values_list=True, is_primeiro=False):
        if len(nm_tabela.split('.')) == 1:
            nm_tabela = self.schema_cliente + '.' + nm_tabela

        set_colunas = ''
        for coluna in lista_colunas_atualizar:
            set_colunas += f" {coluna} = t.{coluna},"
        set_colunas = set_colunas[:-1]  # Removendo a última vírgula

        colunas = ''
        valores = ''
        parametros = {}
        for contador, dict_coluna_valor in enumerate(lista_dict_coluna_valor):
            dict_coluna_valor = self.__montar_log(dict_coluna_valor=dict_coluna_valor)

            if not colunas:
                colunas = ','.join(dict_coluna_valor.keys())

            nm_valores = ''
            for chave, valor in dict_coluna_valor.items():
                parametros[f"{chave}_{contador}"] = valor
                nm_valores += f" :{chave}_{contador},"

            nm_valores = nm_valores[:-1]  # Removendo a última vírgula

            valores += f"({nm_valores}),"
        valores = valores[:-1]  # Removendo a última vírgula

        query = f"""update {nm_tabela} set {set_colunas} from (values {valores}) as t ({colunas})
                    where {nm_tabela}.{nm_pk} = t.{nm_pk};"""

        retorno = self.__query(query=query, parametros=parametros)

        return self.formatar_retorno(retorno=retorno, is_values_list=is_values_list, is_primeiro=is_primeiro)
