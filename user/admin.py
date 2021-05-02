from django.contrib import admin
from django.contrib import admin
from .models import Khach_hang
from import_export.admin import ImportExportModelAdmin
from import_export import resources



class KhachHangAdmin(ImportExportModelAdmin):
    list_display = ('sdt','diachi','tuoi', 'gioi_tinh')


admin.site.register(Khach_hang,KhachHangAdmin)

# Register your models here.
