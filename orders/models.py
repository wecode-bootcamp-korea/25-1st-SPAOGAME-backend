from django.db     import models

from core.models   import TimeStampedModel
from products.models import Color, Size

class Wishlist(TimeStampedModel) :
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta :
        db_table = 'wishlists'

class Basket(TimeStampedModel) :
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product     = models.ForeignKey('products.DetailedProduct', on_delete=models.CASCADE)
    color       = models.ForeignKey('products.Color', on_delete=models.CASCADE)
    size        = models.ForeignKey('products.Size', on_delete=models.CASCADE)    
    quantity    = models.IntegerField(default=1)

    class Meta :
        db_table = 'baskets'