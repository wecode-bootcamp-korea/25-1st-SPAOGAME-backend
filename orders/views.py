import json

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import (
    ObjectDoesNotExist,
    MultipleObjectsReturned
)
from orders.models          import Basket
from products.models        import (
    Size,
    Color,
    DetailedProduct
)
from users.decorators       import login_decorator

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

        except KeyError as e:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except MultipleObjectsReturned:
            return JsonResponse({'MESSAGE':'MULTIPLE_OBJECTS'}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({'MESSAGE':'OBJECT_NOT_EXITST'}, status=400)

    @login_decorator
    def get(self, request):
        try :
            user = request.user
            cart = Basket.objects.filter(user=user)
            
            res  = [{
                    'product_name'          : stuff.product.product.name,
                    'price'                 : stuff.product.product.price,
                    'image'                 : stuff.product.product.thumbnail_image_url,
                    'color'                 : stuff.product.color.name,
                    'size'                  : stuff.product.size.name,
                    'quantity'              : stuff.quantity,
                    'id'                    : stuff.id,
                    'detailed_product_id'   : stuff.product.product.id
                }for stuff in cart]

            return JsonResponse({'res': res}, status=200)
                    
        except TypeError as e :
            return JsonResponse({'MESSAGE': e}, status=400)   

    @login_decorator
    def patch(self, request):
        try:
            data            = json.loads(request.body)
            quantity        = data['quantity']
            product_id      = data['detailed_product_id']
            cart            = Basket.objects.get(product_id=product_id, user_id=request.user)
            cart.quantity   = quantity

            cart.save()
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except MultipleObjectsReturned:
            return JsonResponse({'MESSAGE':'MULTIPLE_OBJECTS'}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({'MESSAGE':'OBJECT_NOT_EXITST'}, status=400)

    @login_decorator
    def delete(self, request):
        try:
            data        = json.loads(request.body)
            basket_id   = data["basket_id"]
            cart        = Basket.objects.get(id=basket_id)

            cart.delete()
            return JsonResponse({'MESSAGE': 'DELETE_SUCCESS'}, status=204)

        except Basket.DoesNotExist:
            return JsonResponse({'MESSAGE': 'NOTING_IN_CART'}, status=404)

        except KeyError as e:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=401)

        except MultipleObjectsReturned:
            return JsonResponse({'MESSAGE':'MULTIPLE_OBJECTS'}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({'MESSAGE':'OBJECT_NOT_EXITST'}, status=400)