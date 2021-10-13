import json
from json.decoder import JSONDecodeError
from django.views import View
from django.http.response import JsonResponse

from postings.models import Posting, Comment
from users.models import User
from products.models import  Image, Product
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
    
class CommentView(View):
    @login_decorator
    def post(self, request):
            try:
                data        = json.loads(request.body)
                user        = request.user
                
                content     = data['content']
                posting_id  = data['posting_id']
                user_id     = user.id
                
                if not (content and posting_id):
                    return JsonResponse({'message' : 'KEY-ERROR'}, status=400)
                
                if not Posting.objects.filter(id = posting_id).exists():
                    return JsonResponse({'message' : "POSTING-DOES-NOT-EXIST"}, status=404)
                
                posting = Posting.objects.get(id = posting_id)
            
                with transaction.atomic():
                    Comment.objects.create(
                        content    = content,
                        user_id    = user_id,
                        posting_id = posting.id
                    )
                
                return JsonResponse({'message' : 'SUCCESS'}, status=200)
            
            except JSONDecodeError:
                return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)