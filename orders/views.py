import json

from django.http import JsonResponse
from django.views import View

from orders.models import Basket
from products.models import Product,DetailedProduct
from users.decorators import login_decorator

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            detailed_product_id = data['product_id']
            quantity   = data['quantity']

            if not DetailedProduct.objects.filter(id=detailed_product_id).exists():
                return JsonResponse({"MESSAGE":"DEATAILED_PRODUCT_DOES_NOT_EXIST"}, status=400)

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

    @login_decorator
    def get(self, request):
        try:
            user = request.user
            cart = Basket.objects.filter(user=user)
            res  = [{
                    'product_name'  : stuff.product.product.name,
                    'price'         : stuff.product.product.price,
                    'image'         : stuff.product.product.thumbnail_image_url,
                    'color'         : stuff.product.color,
                    'size'          : stuff.product.size,
                    'quantity'      : stuff.quantity,
                    'id'            : stuff.id
                }for stuff in cart]
            return JsonResponse({'CART': res}, status=200)

        except KeyError as e:
            return JsonResponse({'MESSAGE': f'{e}'+'_KEY_ERROR'}, status=401)

    @login_decorator
    def delete(self, request, basket_id):
        try:
            cart = Basket.objects.get(id=basket_id)
            cart.delete()
            return JsonResponse({'MESSAGE': 'DELETE_SUCCESS'}, status=204)

        except Basket.DoesNotExist:
            return JsonResponse({'MESSAGE': 'NOTING_IN_CART'}, status=404)

        except KeyError as e:
            return JsonResponse({'MESSAGE': f'{e}'+'_KEY_ERROR'}, status=401)