import json

from django.views     import View
from django.http      import JsonResponse
from django.db.utils  import IntegrityError
from django.db.models import Q

from products.models import (
    Category,
    DetailedProduct,
    Image,
    Menu,
    Product
)

class MenuView(View) :
    def post(self, request) :
        try :
            data = json.loads(request.body)

            menu_name = data['name']

            Menu.objects.create(name=menu_name)

            return JsonResponse({'message':'Save Success'}, status=201)
        
        except KeyError as e : 
            return JsonResponse({'message': f'{e}'}, status=400)

    def get(self, request) :
        try :
            menus = Menu.objects.all()

            menu_lists = []

            for menu in menus :

                menu_lists.append({
                    'id'   : menu.id ,
                    'name' : menu.name
                })

            return JsonResponse({'menus':menu_lists}, status=200)

        except AttributeError as e :
            return JsonResponse({'message': f'{e}'}, status=400)
        
        except TypeError as e :
            return JsonResponse({'message': f'{e}'}, status=400)

class CategoryView(View) :
    def post(self, request) :
        try :
            data = json.loads(request.body)

            menu_id = data['menu_id']
            name    = data['name']

            Category(
                menu_id = menu_id,
                name    = name
            ).save()
        
        except KeyError as e : 
            return JsonResponse({'message': f'{e}'}, status=400)

        except IntegrityError as e :
            return JsonResponse({'message':f'{e}'}, status=200)

    def get(self, request, menu_name) :
        try :
            menu_id = Menu.objects.get(name=menu_name)
            
            categories = Category.objects.filter(menu_id=menu_id)

            category_lists = []

            for category in categories :
                category_lists.append({
                    'menu_id'     : category.menu_id,
                    'category_id' : category.id
                })

            return JsonResponse({'categories':category_lists}, status=200)

        except AttributeError as e :
            return JsonResponse({'message': f'{e}'}, status=400)
        
        except TypeError as e :
            return JsonResponse({'message': f'{e}'}, status=400)

class ProductView(View) :
    def post(self, request) :
        try :
            data = json.loads(request.body)

            name        = data['name']
            price       = data['price']
            description = data['description']
            quantity    = data['quantity']

            products = Product.objects.create(
                name        = name,
                price       = price,
                description = description,
                quantity    = quantity
            )
            
            if data['img_url'] :
                img_urls = data['img_url'] 

                for url in img_urls :
                    Image.objects.create(
                        urls       = url,
                        product_id = products.id
                    )

            return JsonResponse({'message':'hihi'}, status=200)

        except KeyError as e : 
            return JsonResponse({'message': f'{e}'}, status=400)

        except IntegrityError as e :
            return JsonResponse({'message':f'{e}'}, status=200)

    def get(self, request, menu_name, category_name) :
        try :

            menu_id              = Menu.objects.get(name=menu_name).id
            category_id          = Category.objects.get(Q(menu_id=menu_id) & Q(name=category_name))
            detailed_products    = DetailedProduct.objects.filter(Q(menu_id=menu_id) & Q(category_id=category_id)).values('product_id').distinct()

            goods = []

            for detailed_product in detailed_products :

                products = Product.objects.filter(id=detailed_product['product_id'])
                
                for product in products :

                    images = product.image_set.all()

                    url_list = []

                    for urls in images :
                        url_list.append(
                            urls.urls
                        )

                    goods.append({
                        'name'     : product.name,
                        'price'    : product.price,
                        'img_urls' : url_list 
                    })

            return JsonResponse({'goods':goods}, status=200)

        except AttributeError as e :
            return JsonResponse({'message': f'{e}'}, status=400)
        
        except TypeError as e :
            return JsonResponse({'message': f'{e}'}, status=400)