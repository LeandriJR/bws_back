import jwt
from django.conf import settings
from django.http import JsonResponse
from functools import wraps


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
                                'status_code':401
                }, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({
                                'status': False,
                                'descricao': 'Sessão do usuario invalida!',
                                'data': [],
                                'status_code':401
                }, status=401)
        else:
            return JsonResponse({
                                'status': False,
                                'descricao': 'Erro ao autenticar sessão do usuario!',
                                'data': [],
                                'status_code':401
                }, status=401)

        return view_func(request, *args, **kwargs)
    return _wrapped_view
