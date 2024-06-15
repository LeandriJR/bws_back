import http
import time

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView


# Create your views here.
class StatusAPIView(APIView):
    def get(self, request):
        return JsonResponse({'message': 'API is running'}, safe=False, status=http.HTTPStatus.OK)
