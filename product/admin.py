from django.contrib import admin
from .models import Loaisp, San_pham
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class SanPhamAdmin(ImportExportModelAdmin):
    list_display = ('tensp','loaisp','phanloai','gia','xuatxu','soluong','hdsd','mota' ,'anhsp')

class LoaiSPAdmin(ImportExportModelAdmin):
    list_display = ('name','mota')

admin.site.register(San_pham, SanPhamAdmin)
admin.site.register(Loaisp,LoaiSPAdmin)
