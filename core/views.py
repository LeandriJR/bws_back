import http
import time

from django.http import JsonResponse
from rest_framework.views import APIView
from core.mixin import JWTAuthMixin


# Create your views here.
class StatusAPIView(APIView):

    def get(self, request):
        return JsonResponse({'message': 'API is running'}, safe=False, status=http.HTTPStatus.OK)
