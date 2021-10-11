import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spao.settings")

django.setup()

from products.models import (
    Color,
    DetailedProduct,
    Product,
    Size
)

products      = Product.objects.all()
sizes         = Size.objects.all()
colors        = Color.objects.all()

for product in products :

    for size in sizes :

        for color in colors :

            DetailedProduct(
                product_id  = product.id,
                size_id     = size.id,
                color_id    = color.id
            ).save()   