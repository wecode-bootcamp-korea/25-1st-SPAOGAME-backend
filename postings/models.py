from django.db       import models

from core.models     import TimeStampedModel

class Posting(TimeStampedModel):
    user            = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product         = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    title           = models.CharField(max_length = 100)
    content         = models.TextField(null = True)
    rating          = models.IntegerField(null = True)

    class Meta:
        db_table = 'postings'
        
class Comment(TimeStampedModel):
    user            = models.ForeignKey('users.User', on_delete=models.CASCADE)
    posting         = models.ForeignKey(Posting, on_delete=models.CASCADE)
    content         = models.TextField(max_length=200)
  
    class Meta:
        db_table = 'comments'  