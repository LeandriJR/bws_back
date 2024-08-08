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
        retorno = BO.usuario.login.Login(request=request, username=username, password=request.data['password']).login()

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
            endereco_id=self.request.POST.get('endereco_id'),
            cep=self.request.POST.get("cep"),
            rua=self.request.POST.get("rua"),
            numero=self.request.POST.get("numero"),
            complemento=self.request.POST.get("complemento"),
            bairro=self.request.POST.get("bairro"),
            cidade=self.request.POST.get("cidade"),
            ponto_referencia=self.request.POST.get("ponto_referencia"),
            latitude=self.request.POST.get("latitude"),
            longitude=self.request.POST.get("longitude"),
            estado_id=self.request.POST.get("estado_id"),
            estado_sigla=self.request.POST.get("estado_sigla"),
            is_principal=self.request.POST.get("is_principal")
        )

        return JsonResponse(response, safe=False, status=response['status_code'])


class EnderecoDesativarView(JWTAuthMixin, APIView):
    def post(self, request):
        response = BO.usuario.cliente.Cliente().trocar_status_endereco_cliente(
            user_id=self.request.user_logged.get("user_id"),
            endereco_id=self.request.POST.get('endereco_id')
        )

        return JsonResponse(response, safe=False, status=response['status_code'])