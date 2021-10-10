import json
from json.decoder import JSONDecodeError
from django.views import View
from django.http.response import JsonResponse

from postings.models import Posting
from users.models import User
from products.models import  Image, Product
from django.shortcuts import render


class PostingView(View):
    def post(self, request):       
        try:
            data        = json.loads(request.body)
        
            user_id     = data['user_id']
            content     = data['content']
            title       = data.get('title',None)
            product_id  = data['product_id']
            urls        = data.get('urls',None)
        
        
            posting = Posting.objects.create(
                user_id    = user_id,
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

class PostingListView(View) :   
    def get(self,request,product_id):    
        try:
            
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse ({'message':'PRODUCT_DOES_NOT_EXIST'}, status=404)
            
            posting_list = [{
                    'title'     : posting.title,
                    'user_id'   : posting.user_id,
                    'username'  : User.objects.get(id=posting.user_id).username,
                    'content'   : posting.content,
                    'image_url' : [i.image_url for i in Image.objects.filter(posting_id=posting.id)]
                }for posting in Posting.objects.filter(product_id=product_id)
            ]
            
            
            return JsonResponse({'data' : posting_list}, status=201)
        except KeyError :
            return JsonResponse({'message' : 'KEYERROR'}, status=400)
        except ValueError:
            return JsonResponse({'message' : 'DECODE_ERROR'}, status = 400) 
    