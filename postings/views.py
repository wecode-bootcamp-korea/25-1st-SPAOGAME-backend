import json
from json.decoder import JSONDecodeError
from django.views import View
from django.http.response import JsonResponse

from postings.models import Posting
from products.models import  Image
from django.shortcuts import render
from users.decorators import login_decorator
from django.db import transaction 

class PostingView(View):
    @login_decorator
    def post(self, request):       
        try:
            data        = json.loads(request.body)
         
            user_id     = request.user.id
            content     = data.get('content')
            title       = data['title']
            product_id  = data['product_id']
            urls        = data.get('urls',None)
        
            with transaction.atomic():
                posting = Posting.objects.create(
                    user_id    = user_id,
                    content    = content,
                    title      = title,
                    product_id = product_id
                )
                
            Image.objects.bulk_create([Image(urls=image_url, product_id=product_id) for image_url in urls])
            
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError :
            return JsonResponse({'message' : 'KEYERROR'}, status=400)