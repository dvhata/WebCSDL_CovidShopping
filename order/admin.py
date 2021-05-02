from django.contrib import admin
from .models import Don_dat_hang
from import_export.admin import ImportExportModelAdmin

class DonAdmin(ImportExportModelAdmin):
    list_display = ('khach_hang','san_pham','so_luong','ngay_dat','ngay_giao','so_luong','tinh_trang','hinh_thuc_thanh_toan')


admin.site.register(Don_dat_hang,DonAdmin)
# Register your models here.
