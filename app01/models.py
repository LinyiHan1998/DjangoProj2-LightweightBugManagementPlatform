from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(verbose_name='username',max_length=32,db_index=True)
    email = models.EmailField(verbose_name='email',max_length=32)
    mobile_phone = models.CharField(verbose_name='mobile phone',max_length=32)
    password = models.CharField(verbose_name='password',max_length=32)