from django.db     import models

from core.models   import TimeStampedModel

class Menu(TimeStampedModel) :
    name    = models.CharField(max_length=20)

    class Meta :
        db_table = 'menus'

class Category(TimeStampedModel) :
    menu    = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name    = models.CharField(max_length=20)

    class Meta :
        db_table = 'categories'

class Product(TimeStampedModel) :
    name        = models.CharField(max_length=50)
    price       = models.IntegerField(max_length=15)
    description = models.TextField(max_length=1000)
    quantity    = models.IntegerField(max_length=5)

    class Meta :
        db_table = 'products'

class Color(TimeStampedModel) :
    name = models.CharField(max_length=10)

    class Meta :
        db_table = 'colors'

class Size(TimeStampedModel) :
    name = models.CharField(max_length=5)

    class Meta :
        db_table = 'sizes'

class Image(TimeStampedModel) :
    product     = models.ForeignKey(Product,            on_delete=models.CASCADE)
    posting     = models.ForeignKey('postings.Posting', on_delete=models.CASCADE, null=True)
    urls        = models.CharField(max_length=700)

    class Meta :
        db_table = 'images'

class DetailedProduct(TimeStampedModel) :
    menu         = models.ForeignKey(Menu,         on_delete=models.CASCADE)
    category     = models.ForeignKey(Category,     on_delete=models.CASCADE)
    color        = models.ForeignKey(Color,        on_delete=models.CASCADE)
    size         = models.ForeignKey(Size,         on_delete=models.CASCADE)
    product      = models.ForeignKey(Product,      on_delete=models.CASCADE)

    class Meta : 
        db_table = 'detailed_products'