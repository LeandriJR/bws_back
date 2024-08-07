from django.utils.decorators import method_decorator
from core.decorators import jwt_required


class JWTAuthMixin:
    @method_decorator(jwt_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)