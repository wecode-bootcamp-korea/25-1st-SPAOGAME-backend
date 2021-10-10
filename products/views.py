import json

from django.views     import View
from django.http      import JsonResponse
from django.db.utils  import IntegrityError
from django.db.models import Q

from postings.models import (
    Comment,
    Posting
)

from products.models import (
    Category,
    Color,
    DetailedProduct,
    Image,
    Menu,
    Product,
    Size
)

from users.models    import User

class MenuView(View) :
    def post(self, request) :
        try :
            data      = json.loads(request.body)
            menu_name = data['name']

            Menu.objects.create(name=menu_name)

            return JsonResponse({'message':'Save Success'}, status=201)
        
        except KeyError as e : 
            return JsonResponse({'message': e}, status=400)

    def get(self, request) :
        try :
            menus      = Menu.objects.all()
            menu_lists = []

            for menu in menus :

                menu_lists.append({
                    'id'   : menu.id ,
                    'name' : menu.name
                })

            return JsonResponse({'menus':menu_lists}, status=200)

        except AttributeError as e :
            return JsonResponse({'message': e}, status=400)
        
        except TypeError as e :
            return JsonResponse({'message': e}, status=400)

class CategoryView(View) :
    def post(self, request) :
        try :
            data    = json.loads(request.body)
            menu_id = data['menu_id']
            name    = data['name']

            Category(
                menu_id = menu_id,
                name    = name
            ).save()
        
        except KeyError as e : 
            return JsonResponse({'message': e}, status=400)

        except IntegrityError as e :
            return JsonResponse({'message':e}, status=200)

    def get(self, request, menu_name) :
        try :
            menu_id        = Menu.objects.get(name=menu_name)
            categories     = Category.objects.filter(menu_id=menu_id)
            category_lists = []

            for category in categories :
                category_lists.append({
                    'menu_id'     : category.menu_id,
                    'category_id' : category.id
                })

            return JsonResponse({'categories':category_lists}, status=200)

        except AttributeError as e :
            return JsonResponse({'message': e}, status=400)
        
        except TypeError as e :
            return JsonResponse({'message': e}, status=400)

class ProductView(View) :
    def post(self, request) :
        try :
            data        = json.loads(request.body)
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

            return JsonResponse({'message':'Save Success'}, status=200)

        except KeyError as e : 
            return JsonResponse({'message': e}, status=400)

        except IntegrityError as e :
            return JsonResponse({'message': e}, status=200)

    def get(self, request, menu_name, category_name) :
        try :
            offset = int(request.GET.get('offset',0)) 
            limit  = int(request.GET.get('limit', 0))

            if limit-offset > 20 :
                return JsonResponse({'message':'too much lists'}, status=400)

            menu_id              = Menu.objects.get(name=menu_name).id
            category_id          = Category.objects.get(Q(menu_id=menu_id) & Q(name=category_name))
            detailed_products    = DetailedProduct.objects.filter(Q(menu_id=menu_id) & Q(category_id=category_id)).values('product_id').distinct().order_by('product_id')[offset:offset+limit]
            goods                = []

            for detailed_product in detailed_products :

                products = Product.objects.filter(id=detailed_product['product_id'])
                
                for product in products :

                    images   = product.image_set.all()

                    postings = product.posting_set.all()
                    
                    colors   = DetailedProduct.objects.filter(product_id=product.id).values('color_id').distinct()[:4]
                    
                    color_list = []

                    for color in colors :
                        color_list.append(
                            Color.objects.get(id=color['color_id']).name
                        )

                    url_list = []

                    for urls in images :
                        url_list.append(
                            urls.urls
                        )

                    goods.append({
                        'id'           : product.id,
                        'name'         : product.name,
                        'price'        : product.price,
                        'img_urls'     : url_list,
                        'review_count' : postings.count(),
                        'colors'       : color_list
                    })

            return JsonResponse({'goods':goods}, status=200)

        except AttributeError as e :
            return JsonResponse({'message': e}, status=400)
        
        except TypeError as e :
            return JsonResponse({'message': e}, status=400)

class DetailProductView(View) :
    def get(self, request, id) :
        try : 
            detailed_products = DetailedProduct.objects.filter(product_id=id)
            colors            = DetailedProduct.objects.filter(product_id=id).values('color_id').distinct()[:4]
            sizes             = DetailedProduct.objects.filter(product_id=id).values('size_id').distinct()
            posting_count     = Posting.objects.filter(product_id=id).count()
            goods_detail      = []

            for detail_info in detailed_products :

                color_list   = []

                for color in colors :
                    
                    color_list.append(
                        Color.objects.get(id=color['color_id']).name
                    )

                sizes_list = []

                for size in sizes :

                    sizes_list.append(
                        Size.objects.get(id=size['size_id']).name
                    )

                product_images = Image.objects.filter(product_id=detail_info.product_id).distinct()

                image_list = []

                for image in product_images :

                    image_list.append(image.urls)

                postings = Posting.objects.filter(product_id=id).order_by('-created_at')

                posting_info = []
                comment_info = []

                for posting in postings :
                    
                    posting_images = Image.objects.filter(posting_id=posting.id)

                    posting_image_list  = []

                    for image in posting_images : 
                        posting_image_list.append(image.urls)

                    posting_info.append({
                        "posting_id"      : posting.id,
                        "posting_writer"  : User.objects.get(id=posting.user_id).name,
                        "posting_title"   : posting.title,
                        "posting_content" : posting.content,
                        "posting_image"   : posting_image_list,
                        "posting_date"    : posting.created_at.strftime('%Y-%m-%d')
                    })

                    comments = Comment.objects.filter(posting_id=posting.id).order_by('created_at')

                    for comment in comments :

                        comment_info.append({
                            "posting_id"      : posting.id,
                            "comment_id"      : comment.id,
                            "comment_writer"  : User.objects.get(id=comment.user_id).name,
                            "comment_content" : comment.content,
                            "comment_date"    : comment.created_at.strftime('%Y-%m-%d')
                        })

            goods_detail.append({
                "product_id"    : id,
                "name"          : Product.objects.get(id=id).name,
                "price"         : Product.objects.get(id=id).price,
                "colors"        : color_list,
                "size"          : sizes_list,
                "image_list"    : image_list,
                "posting_info"  : posting_info,
                "posting_count" : posting_count,
                "comment_info"  : comment_info
            })
                    
            return JsonResponse({'goods_detail':goods_detail}, status=200)

        except AttributeError as e :
            return JsonResponse({'message': e}, status=400)
        
        except TypeError as e :
            return JsonResponse({'message': e}, status=400)