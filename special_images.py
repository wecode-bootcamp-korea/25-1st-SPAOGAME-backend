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
    'https://www.elandrs.com/upload/fckeditor/tempgoodsdesc/2021041618889852014.jpg',
    'https://www.elandrs.com/upload/fckeditor/tempgoodsdesc/2021041619762748826.jpg'
    'http://spao.com/web/upload/NNEditor/20211005/EBB2A0EC8AA4ED8AB8EBA6ACEBB7B0EC96B4_9EC9B94_01.jpg',
    'http://spao.com/web/upload/NNEditor/20211005/EBB2A0EC8AA4ED8AB8EBA6ACEBB7B0EC96B4_9EC9B94_02.jpg',
    'http://spao.com/web/upload/NNEditor/20201118/%EB%A6%AC%EB%B7%B0%EC%95%88%EB%82%B4_01_shop1_084423.jpg',
]

for url in images :
    Image(
        urls = url,
        product_id=13
    ).save()