import json, re

from django.db.models.fields import GenericIPAddressField
import bcrypt, jwt

from django.http import JsonResponse
from django.views import View

from users.models import User
from my_settings import MY_SECRET_KEY, MY_ALGORITHMS


class SignupView(View):
    def post(self, request):
        try:
            data                = json.loads(request.body)
            username            = data['username']
            password            = data['password']
            name                = data['name']
            email               = data['email']
            mobile_number       = data['mobile_number']
            address1            = data['address1']
            address2            = data['address2']
            birthday            = data['birthday']
            gender              = data['gender']

            email_validation    = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            password_validation = re.compile("^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%*^&+=]).*$")

            if not email_validation.match(email):
                return JsonResponse({"MESSAGE":"EMAIL_VALIDATION_ERROR"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"MESSAGE":"DUPLICATION_ERROR"}, status=400)

            if not password_validation.match(password):
                return JsonResponse({"MESSAGE":"PASSWORD_VALIDATION_ERROR"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_password = hashed_password.decode('utf-8')

            User.objects.create(
                username            = data['username'],
                password            = decoded_hashed_password,
                name                = data['name'],
                email               = data['email'],
                mobile_number       = data['mobile_number'],
                address1            = data['address1'],
                address2            = data['address2'],
                birthday            = data['birthday'],
                gender              = data['gender']
            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)






