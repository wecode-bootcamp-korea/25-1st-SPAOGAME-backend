import json

from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from orders.models import Basket
from products.models import Size, Color, DetailedProduct
from users.decorators import login_decorator

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data                = json.loads(request.body)
            product_id          = data['product_id']
            color_id            = Color.objects.get(name=data['color_name']).id
            size_id             = Size.objects.get(name=data['size_name']).id
            detailed_product    = DetailedProduct.objects.get(product_id=product_id,
                                                                color_id=color_id,
                                                                size_id =size_id)
            quantity            = data['quantity']

            if not DetailedProduct.objects.filter(id=detailed_product.id).exists():
                return JsonResponse({"MESSAGE":"DOES_NOT_EXIST"}, status=400)

            if Basket.objects.filter(product_id=detailed_product.id).exists():
                return JsonResponse({"MESSAGE":"ALREADY_EXIST"}, status=400)

            Basket.objects.create(
                user       = request.user,
                product_id = detailed_product.id,
                quantity   = quantity,
                )
            return JsonResponse({'MESSAGE':'CREATE_BASKET'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except MultipleObjectsReturned:
            return JsonResponse({'MESSAGE':'MULTIPLE_OBJECTS'}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({'MESSAGE':'OBJECT_NOT_EXITST'}, status=400)


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
