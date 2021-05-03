from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#default = User.objects.filter(username="")

class Khach_hang(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=50)
    sdt = models.CharField(default="", max_length= 15)
    diachi = models.CharField(default="",max_length= 200)
    tuoi = models.IntegerField(default= 0)
    gioi_tinh = models.CharField(default="",max_length=15)