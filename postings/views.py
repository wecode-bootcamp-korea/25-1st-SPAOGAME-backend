import json
from json.decoder import JSONDecodeError
from django.views import View
from django.http.response import JsonResponse

from postings.models import Posting, Comment
from users.models import User
from products.models import  Image, Product
from django.shortcuts import render
from users.decorators import login_decorator


class PostingView(View):
    @login_decorator
    def post(self, request):       
        try:
            data        = json.loads(request.body)
         
            user_id     = data['user_id']
            content     = data['content']
            title       = data.get('title',None)
            product_id  = data['product_id']
            urls        = data.get('urls',None)
        
            posting = Posting.objects.create(
                user_id    = User.objects.get(id = request.user.id),
                content    = content,
                title      = title,
                product_id = product_id
            )
            
            if urls :
                for image_url in urls :
                    Image.objects.create(
                        image_url = image_url,
                        posting   = posting
                    ) 
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError :
            return JsonResponse({'message' : 'KEYERROR'}, status=400)
    
class CommentView(View):
    @login_decorator
    def post(self, request):
            try:
                data=json.loads(request.body)
                user = request.user
                
                content = data.get('content', None)
                posting_id = data.get('posting_id', None)
                
                if not (content and posting_id):
                    return JsonResponse({'message':'KEY-ERROR'}, status=400)
                
                if not Posting.objects.filter(id=posting_id).exists():
                    return JsonResponse({'message':"POSTING-DOES-NOT-EXIST"}, status=404)
                
                posting = Posting.objects.get(id=posting_id)
            
                Comment.objects.create(
                    content = content,
                    user = user,
                    posting = posting
                )
                
                return JsonResponse({'message':'SUCCESS'}, status=200)
            
            except JSONDecodeError:
                return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)