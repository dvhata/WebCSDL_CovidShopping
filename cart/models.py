from django.db import models
from user.models import Khach_hang
from product.models import San_pham
# Create your models here.

class gio_hang(models.Model):
    khach_hang = models.ForeignKey(Khach_hang,on_delete=models.CASCADE)
    san_pham = models.ForeignKey(San_pham, on_delete=models.CASCADE)
    so_luong = models.IntegerField(default=0)
