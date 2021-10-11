import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spao.settings")
django.setup()

from products.models import Image

images = [
    'http://spao.com/web/product/small/202108/504512a2f6a19164be6fcb40b04b1bec.jpg',
    'http://spao.com/web/product/extra/small/202108/85bcadb79d42d3d51deaa27a3cb59eb0.jpg',
    'http://spao.com/web/product/extra/small/202108/e0f67f571208ae84ec6b8a0d3ca40ff8.jpg',
    'http://spao.com/web/product/extra/small/202108/b5b47c7f246c0a1564e52e2d17a41235.jpg',
    'http://spao.com/web/product/extra/small/202108/3df208f9655c478e2804edf933a8cec1.jpg',
    'http://spao.com/web/product/extra/small/202108/cc7a3d4e587f0d94905cbeaef2a540ae.jpg',
]

for url in images :
    Image(
        urls = url,
        product_id=2
    ).save()