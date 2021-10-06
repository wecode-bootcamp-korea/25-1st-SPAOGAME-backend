import json

import bcrypt
import jwt

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError
from json.decoder           import JSONDecodeError

from users.validation       import validate_email, validate_password
from users.models           import User
from my_settings            import MY_SECRET_KEY, MY_ALGORITMHS

class SignUp(View):
    def post(self, request):
        try :
            data            = json.loads(request.body)
            name            = data['name']
            email           = data['email']
            password        = data['password']
            mobile_number   = data['mobile_number']
            

            validate_email(email)
            validate_password(password)
            
            if User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE':'ALREADY_EXISTS_EMAIL'}, status=404)
            
            hashed_pw         = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_pw = hashed_pw.decode('utf-8')
            
            User.objects.create(
                name         = name,
                email        = email,
                password     = decoded_hashed_pw,
                phone_number = phone_number,
                blog_url     = blog_url,
            )

            return JsonResponse({'MESSAGE':'SUCCESS'} , status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"}, status = 400)
        
        except ValidationError as e:
            return JsonResponse({'MESSAGE':(e.message)}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'MESSAGE':'JSON_DECODE_ERROR'}, status=400)

class SignIn(View):
    def get(self, request):
        try :
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email = email).exists() :
                return JsonResponse({'MESSAGE':'INVALID_USER_EMAIL'}, status = 401)
            
            user = User.objects.get(email = email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')) :
                return JsonResponse({'MESSAGE':'INVALID_USER_PASSWORD'}, status = 401)
            
            access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm = ALGORITHM)

            return JsonResponse({'ACCESS_TOKEN' : access_token}, status = 200)

        except KeyError :
            return JsonResponse({'MESSAGE':"KEY_ERROR"}, status = 400)
        
        except JSONDecodeError :
            return JsonResponse({'MESSAGE':'JSON_DECODE_ERROR'}, status = 400)
        
        except User.DoesNotExist :
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status = 401)