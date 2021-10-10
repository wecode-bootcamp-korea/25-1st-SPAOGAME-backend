import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spao.settings")

django.setup()

from products.models import (
    Category,
    Color,
    DetailedProduct,
    Menu,
    Product,
    Size
)

menu_name     = 'women'
category_name = 'outer'
menu_id       = Menu.objects.get(name=menu_name).id
category_id   = Category.objects.get(menu_id=menu_id, name=category_name).id

products      = Product.objects.all()
sizes         = Size.objects.all()
colors        = Color.objects.all()

for product in products :

    for size in sizes :

        for color in colors :

            DetailedProduct(
                menu_id     = menu_id,
                category_id = category_id,
                product_id  = product.id,
                size_id     = size.id,
                color_id    = color.id
            ).save()   