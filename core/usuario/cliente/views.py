import json

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
import BO.usuario.cliente
import BO.usuario.login
import BO.usuario.register
import core.usuario.models
from core.mixin import JWTAuthMixin


# Create your views here.


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = BO.usuario.cliente.Cliente().buscar_username_login(request.data['email'])
        user = BO.usuario.login.Login(request=request, username=username, password=request.data['password']).login()

        retorno = BO.usuario.cliente.Cliente().buscar_informacao(user['data']['user']),

        return JsonResponse(retorno, safe=False, status=retorno['status_code'])


class RegisterUserView(APIView):
    def post(self, request):
        response = BO.usuario.register.Register().registrar(response=request.data)
        return JsonResponse(response, safe=False, status=response['status_code'])


class EnderecoView(JWTAuthMixin, APIView):
    def get(self, request):
        response = BO.usuario.cliente.Cliente().buscar_endereco_cliente(
            user_id=self.request.user_logged.get("user_id")
        )

        return JsonResponse(response, safe=False, status=response['status_code'])

    def post(self, request):
        response = BO.usuario.cliente.Cliente().salvar_endereco_usuario(
            user_id=self.request.user_logged.get("user_id"),
            endereco_id=self.request.data.get('endereco_id'),
            cep=self.request.data.get("cep"),
            rua=self.request.data.get("rua"),
            numero=self.request.data.get("numero"),
            complemento=self.request.data.get("complemento"),
            bairro=self.request.data.get("bairro"),
            cidade=self.request.data.get("cidade"),
            ponto_referencia=self.request.data.get("ponto_referencia"),
            latitude=self.request.data.get("latitude"),
            longitude=self.request.data.get("longitude"),
            estado_id=self.request.data.get("estado_id"),
            estado_sigla=self.request.data.get("estado_sigla"),
            is_principal=self.request.data.get("is_principal")
        )

        return JsonResponse(response, safe=False, status=response['status_code'])


class EnderecoDesativarView(JWTAuthMixin, APIView):
    def post(self, request):
        response = BO.usuario.cliente.Cliente().trocar_status_endereco_cliente(
            user_id=self.request.user_logged.get("user_id"),
            endereco_id=self.request.data.get('endereco_id')
        )

        return JsonResponse(response, safe=False, status=response['status_code'])
