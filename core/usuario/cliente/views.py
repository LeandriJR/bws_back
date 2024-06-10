import json

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
import BO.usuario.cliente
import BO.usuario.login
import BO.usuario.register
import core.usuario.models
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