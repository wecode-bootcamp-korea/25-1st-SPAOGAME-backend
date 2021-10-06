from django.db import models

class TimeStampedModel(models.Model) :
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(default = None)
    deleted_at = models.DateTimeField(default = None)

    class Meta :
        abstract = True

class Gender(TimeStampedModel) :
    name          = models.CharField(max_length=100)

    class Meta :
        db_table = "genders"

class User(TimeStampedModel) :
    username        = models.CharField(max_length=200)
    password        = models.CharField(max_length=200)
    name            = models.CharField(max_length=100)
    email           = models.CharField(max_length=200, unique=True)
    mobile_number   = models.IntegerField()
    address1        = models.CharField(max_length=450)
    address2        = models.CharField(max_length=450)
    birthday        = models.DateTimeField
    gender          = models.ForeignKey(Gender, on_delete=models.CASCADE)

    class Meta :
        db_table = "users"
