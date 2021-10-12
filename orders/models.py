from django.db     import models

from core.models   import TimeStampedModel

class Wishlist(TimeStampedModel) :
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta :
        db_table = 'wishlists'

class Basket(TimeStampedModel) :
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product     = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    color       = models.ForeignKey('products.DetailedProduct', related_name='basket_color', on_delete=models.CASCADE)
    size        = models.ForeignKey('products.DetailedProduct', related_name='basket_size', on_delete=models.CASCADE)    
    quantity    = models.IntegerField(default=1)

    class Meta :
        db_table = 'baskets'