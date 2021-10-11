import json, re
import bcrypt, jwt

from django.http import JsonResponse
from django.views import View

from users.models import User, Gender
from my_settings import MY_SECRET_KEY, MY_ALGORITHMS

class SignUpView(View):
    def post(self, request):
        try:
            data                = json.loads(request.body)
            
            username            = data['username']
            password            = data['password']
            name                = data['name']
            email               = data['email']
            mobile_number       = data['mobile_number']
            address1            = data['address1']
            address2            = data.get['address2',None]
            birthday            = data['birthday']
            gender              = data.get['gender',None]

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
                username            = username,
                password            = decoded_hashed_password,
                name                = name,
                email               = email,
                mobile_number       = mobile_number,
                address1            = address1,
                address2            = address2,
                birthday            = birthday,
                gender              = Gender.objects.get(id=gender)
            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email          = data['email']
            password       = data['password']

            if not (email and password):
                return JsonResponse({'MESSAGE':'EMPTY_VALUE'}, status=400)
                
            if not User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE':'USER_DOES_NOT_EXIST'}, status=401)
            
            user = User.objects.get(email=email)
                
            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

            token = jwt.encode({'id' : user.id}, MY_SECRET_KEY, MY_ALGORITHMS)
            
            return JsonResponse({'MESSAGE':'SUCCESS', 'TOKEN' : token}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)