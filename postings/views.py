import json
from json.decoder import JSONDecodeError
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.http.response import JsonResponse

from postings.models import Posting, Comment
from products.models import  Image, Product
from users.decorators import login_decorator
from users.models import User
from django.db import transaction
class PostingView(View):
  #  @login_decorator
  # 데코레이터 적용 후에도 해보기
    def post(self, request):
        try:
            data        = json.loads(request.body)
            # user_id     = request.user.id
            content     = data['review_content']
            title       = data['title']
            product_id  = data['product_id']
            print(data)

            with transaction.atomic():
                Posting.objects.create(
                    user_id    = int(1) , 
                    content    = content,
                    title      = title,
                    product_id = Product.objects.get(id=product_id).id
                )
   
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError :
            return JsonResponse({'message' : 'KEYERROR'}, status=400)

class CommentView(View):
  #  @login_decorator
    def post(self, request):
            try:
                data        = json.loads(request.body)
              #  user        = request.user
                content     = data['comment_content']
                posting_id  = data['posting_id']
                print(data)
                
                if not (content and posting_id):
                    return JsonResponse({'message' : 'KEY-ERROR'}, status=400)

                if not Posting.objects.filter(id = posting_id).exists():
                    return JsonResponse({'message' : "POSTING-DOES-NOT-EXIST"}, status=404)

                posting = Posting.objects.get(id = posting_id)

                with transaction.atomic():
                    Comment.objects.create(
                        content    = content,
                        user_id    = int(1),
                        posting_id = posting.id
                    )
                return JsonResponse({'message' : 'SUCCESS'}, status=200)

            except JSONDecodeError:
                return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)

class CommentDeleteView(View) :
    #@deco
  # decorator 넣어야함
    def delete(self, request, comment_id):
        try:
            print(comment_id)
            Comment.objects.filter(id = comment_id).delete()
            return JsonResponse({'message' : 'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message' : 'KEY-ERROR'}, status=400)
