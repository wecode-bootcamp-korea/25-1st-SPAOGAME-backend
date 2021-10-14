import json
from json.decoder         import JSONDecodeError
from django.views         import View
from django.http.response import JsonResponse

from postings.models      import (
    Posting,
    Comment
)
from products.models      import  (
    Image,
    Product
)
from users.decorators     import login_decorator
from django.db            import transaction

class PostingView(View):
    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            user_id     = request.user.id
            content     = data['review_content']
            title       = data['title']
            product_id  = data['product_id']

            with transaction.atomic():
                Posting.objects.create(
                    user_id    = user_id , 
                    content    = content,
                    title      = title,
                    product_id = product_id
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
                data        = json.loads(request.body)
                user_id     = request.user
                content     = data['comment_content']
                posting_id  = data['posting_id']
                
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

class CommentDeleteView(View) :
    @login_decorator
    def delete(self, request, comment_id):
        try:
            Comment.objects.filter(id = comment_id).delete()
            return JsonResponse({'message' : 'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message' : 'KEY-ERROR'}, status=400)
