from django.db import models
from django.conf import settings
# Create your models here.

class Khach_hang(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=50)
    sdt = models.CharField(default="", max_length= 15)
    diachi = models.CharField(default="",max_length= 200)
    tuoi = models.IntegerField(default= 0)
    gioi_tinh = models.CharField(default="",max_length=15)