from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

import BO.usuario.login
import BO.usuario.funcionario

# Create your views here.


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        retorno = BO.usuario.login.Login(request=request, username=request.data['username'], password=request.data['password']).login()
        if retorno['status']:
            retorno = BO.usuario.funcionario.Funcionario().buscar_informacao(user=retorno['data']['user'])
        return JsonResponse(retorno, safe=False, status=retorno['status_code'])
