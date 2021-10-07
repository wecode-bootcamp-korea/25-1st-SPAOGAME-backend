from django.db      import models

from core.models    import TimeStampedModel

class Gender(TimeStampedModel) :
    name          = models.CharField(max_length = 100)

    class Meta :
        db_table = "genders"

class User(TimeStampedModel) :
    username        = models.CharField(max_length = 200)
    password        = models.CharField(max_length = 200)
    name            = models.CharField(max_length = 100)
    email           = models.CharField(max_length = 200, unique=True)
    mobile_number   = models.IntegerField()
    address1        = models.CharField(max_length = 450)
    address2        = models.CharField(max_length = 450, null = True)
    birthday        = models.DateField()
    gender          = models.ForeignKey(Gender, on_delete = models.CASCADE, null = True)

    class Meta :
        db_table = "users"