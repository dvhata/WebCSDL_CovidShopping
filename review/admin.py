from django.contrib import admin
from .models import Nhan_xet
from import_export.admin import ImportExportModelAdmin
from import_export import resources



class NhanXetAdmin(ImportExportModelAdmin):
    list_display = ('khach_hang','san_pham','binh_luan','diem','thoi_gian')


admin.site.register(Nhan_xet,NhanXetAdmin)

# Register your models here.
