from django.db     import models

from core.models   import TimeStampedModel

class Wishlist(TimeStampedModel) :
    user    = models.ForeignKey('users.User',       on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta :
        db_table = 'wishlists'

class Basket(TimeStampedModel) :
    user    = models.ForeignKey('users.User',       on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta :
        db_table = 'baskets'