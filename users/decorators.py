import jwt

from django.conf import settings
from django.http import JsonResponse
from my_settings import MY_SECRET_KEY, MY_ALGORITHMS

from .models import User

def login_decorator(func):
    def wraper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            token = jwt.decode(access_token, MY_SECRET_KEY, MY_ALGORITHMS)
            user = User.objects.get(id=token['id'])
            request.user = user
        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE': 'DECODE_ERROR'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'USER_NOTEXIST'}, status=401)
        return func(self, request, *args, **kwargs)
    return wraper