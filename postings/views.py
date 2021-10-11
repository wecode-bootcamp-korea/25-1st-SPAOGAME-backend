import json
from json.decoder import JSONDecodeError
from django.views import View
from django.http.response import JsonResponse

from postings.models import Posting
from products.models import  Image
from django.shortcuts import render


class PostingView(View):
    def post(self, request):       
        try:
            data        = json.loads(request.body)
        
            user_id     = data['user_id']
            content     = data.get('content',None)
            title       = data['title']
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
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError :
            return JsonResponse({'message':'KEYERROR'}, status=400)