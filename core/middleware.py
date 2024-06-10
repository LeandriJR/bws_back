from bws_back.settings import DB_CONNECTIONS
import threading
from django.http import HttpRequest


class SqlAlchemySessionMiddleware:
    def __init__(self, get_response):
        self.session = DB_CONNECTIONS['default']['sessoes']
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # request.db_session = self.session()
        return response

        # try:
        #     session = request.db_session
        # except AttributeError:
        #     return response
        # else:
        #     if getattr(request, '_exception', None) is None:
        #         session.commit()
        # session.close()


class GlobalRequestStorage:
    storage = threading.local()

    def get(self):
        if hasattr(self.storage, "request"):
            return self.storage.request
        else:
            return None

    def get_user(self, request=None):
        request = request or self.get()
        return getattr(request, "user", None)

    def get_user_id(self, request=None):
        request = request or self.get()
        return getattr(request, "user_id", None)

    def set(self, request):
        self.storage.request = request

    def set_user(self, user, request=None):
        if request:
            self.storage.request = request
        if not hasattr(self.storage, "request"):
            self.storage.request = HttpRequest()
        if user:
            self.storage.request.user = user

    def recover(self, request=None, user=None):
        if hasattr(self.storage, "request"):
            del self.storage.request
        if request is not None:
            self.storage.request = request
            if user:
                self.storage.request.user = user


class GlobalRequest:
    def __init__(self, request=None, user=None):
        self.global_request_storage = GlobalRequestStorage()
        self.new_request = request or HttpRequest()
        self.new_user = user
        self.old_request = self.global_request_storage.get()
        self.old_user = self.global_request_storage.get_user(self.old_request)

    def __enter__(self):
        self.global_request_storage.set_user(user=self.new_user, request=self.new_request)
        return self.global_request_storage.get()

    def __exit__(self, *args, **kwargs):
        self.global_request_storage.recover(request=self.old_request, user=self.old_user)


class GlobalRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with GlobalRequest(request=request):
            return self.get_response(request)


def get_schema_cliente():
    request = GlobalRequestStorage().get()
    return request.tenant.schema_name

