from django.db import models
from user.models import Khach_hang
from product.models import San_pham


# Create your models here.

class Nhan_xet(models.Model):
    khach_hang = models.ForeignKey(Khach_hang, on_delete= models.CASCADE)
    san_pham = models.ForeignKey(San_pham, on_delete= models.CASCADE)
    binh_luan = models.TextField(default="")
    diem = models.IntegerField(default = 10)
    thoi_gian = models.DateField()
