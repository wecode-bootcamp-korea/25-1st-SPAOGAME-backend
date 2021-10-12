import json

from django.http import JsonResponse
from django.views import View

from orders.models import Basket
from products.models import Product
from users.decorators import login_decorator

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            detailed_product_id = data['product_id']
            quantity   = data['quantity']

            if not Product.objects.filter(id=detailed_product_id).exists():
                return JsonResponse({"MESSAGE":"DOES_NOT_EXIST"}, status=400)

            if Basket.objects.filter(product_id=detailed_product_id).exists():
                return JsonResponse({"MESSAGE":"ALREADY_EXIST"}, status=400)

            Basket.objects.create(
                user       = request.user,
                product_id = detailed_product_id,
                quantity   = quantity,
                )

            return JsonResponse({'MESSAGE':'CREATE_BASKET'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)