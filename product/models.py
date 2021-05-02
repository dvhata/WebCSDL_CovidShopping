from django.db import models

# Create your models here.


class Loaisp(models.Model):
    name = models.CharField(default='', max_length= 200)
    mota= models.TextField(default='')

    def __str__(self):
        return self.name

class San_pham(models.Model):
    #msp = models.CharField(max_length = 50 )
    tensp = models.CharField(default="", max_length= 200)
    loaisp = models.ForeignKey(Loaisp, on_delete=models.CASCADE )
    phanloai = models.CharField(default="", max_length= 200)
    gia = models.IntegerField()
    xuatxu = models.CharField(default="", max_length=50)
    thuonghieu = models.CharField(default="", max_length= 200)
    soluong = models.IntegerField()
    hdsd= models.TextField(default="")
    mota= models.TextField(default="")
    anhsp = models.ImageField(upload_to='product_pictures')

    def __str__(self):
        return self.tensp
