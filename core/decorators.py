import http

import jwt
from django.conf import settings
from django.http import JsonResponse
from functools import wraps
import inspect
from typing import Callable
from BO.base.excecao import ValidationError

def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = {
                    'user_id': payload['user_id'],
                    'username': payload['username'],
                    'email': payload['email'],
                    'is_active': True
                }
                request.user_logged = user
            except jwt.ExpiredSignatureError:
                return JsonResponse({
                                'status': False,
                                'descricao': 'Sessão do usuario expirada!',
                                'data': [],
                                'status_code': 401
                }, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({
                                'status': False,
                                'descricao': 'Sessão do usuario invalida!',
                                'data': [],
                                'status_code': 401
                }, status=401)
        else:
            return JsonResponse({
                                'status': False,
                                'descricao': 'Erro ao autenticar sessão do usuario!',
                                'data': [],
                                'status_code': 401
                }, status=401)

        return view_func(request, *args, **kwargs)
    return _wrapped_view



class Response:
    def __init__(
            self,
            desc_error: str = '',
            desc_success: str = '',
            lista_retornos: list = None,
            is_salvar_log: bool = True,
            is_manter_retorno: bool = False,
    ):
        self.desc_success = desc_success
        self.desc_error = desc_error
        self.lista_retornos = lista_retornos or []
        self.is_salvar_log = is_salvar_log
        self.is_manter_retorno = is_manter_retorno

    def __call__(self, funcao) -> Callable[..., dict]:
        def wrapper(*args, **kwargs):
            response = {
                'status': True,
                'status_code': http.HTTPStatus.OK,
                'descricao': self.desc_success,
                'data': {}
            }
            retorno = None
            try:
                retorno = funcao(*args, **kwargs)

            except ValidationError as e:
                # FUNÇÂO DE SALVAR LOG DE ERRO NO FUTURO

                response['status'] = False
                response['status_code'] = e.status_code
                response['descricao'] = e.mensagem
                retorno = e.retorno

            except Exception as e:
                response['status'] = False
                response['status_code'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
                response['descricao'] = self.desc_error
                response['data'] = []

                return response
            if self.is_manter_retorno:
                return retorno

            if retorno is not None:
                try:
                    if not self.lista_retornos:
                        response['retorno'] = retorno

                    elif isinstance(retorno, dict):
                        response['data'][self.lista_retornos[0]] = retorno

                    elif isinstance(retorno, tuple):
                        for nm_chave, valor in zip(self.lista_retornos, retorno):
                            response['data'][nm_chave] = valor

                    elif len(self.lista_retornos) == 1:
                        response['data'][self.lista_retornos[0]] = retorno

                except Exception as e:
                    response['status'] = False
                    response['status_code'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
                    response['descricao'] = 'Erro no decorator'
                    response['data'] = []
            else:
                if self.lista_retornos:
                    for retorno in self.lista_retornos:
                        response['data'][retorno] = None

            return response

        # Add the decorator parameters to the wrapper function's signature
        wrapper.__signature__ = inspect.signature(funcao)

        return wrapper

