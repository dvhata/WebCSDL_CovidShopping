from django.db import models
from user.models import Khach_hang
from product.models import San_pham

# Create your models here.

class Don_dat_hang(models.Model):
    khach_hang = models.ForeignKey(Khach_hang, on_delete= models.CASCADE,default=None)
    san_pham = models.ForeignKey(San_pham, on_delete= models.CASCADE,default=None)
    so_luong = models.IntegerField(default=0)
    ngay_dat = models.DateField(default=None)
    ngay_giao = models.DateField(default=None)
    so_luong = models.IntegerField(default=0)
    tinh_trang = models.CharField(default="", max_length = 50)
    hinh_thuc_thanh_toan = models.CharField(default="", max_length = 100)