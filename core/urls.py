from django.urls import path, include
from .views import HomeView,SanphamView,Index
from django.conf import settings
from django.conf.urls.static import static
from . import views as core_view
from profiles import views as profiles_views


urlpatterns = [
    path('sanpham/',SanphamView.as_view(), name = 'sanpham'),
    path('sanphamcuthe/<int:sanpham_id>',Index.as_view(), name = 'sanphamcuthe' ),
    path('sanpham/<int:loaisp_id>', core_view.loaispview, name = "loc_loaisp" ),
    path('accounts/', include('django.contrib.auth.urls')),
    path('giohang/',core_view.giohangview , name = 'giohang'),
    path('',HomeView.as_view(), name = 'Trangchu'),
    path('login/', core_view.SiteLoginView.as_view(), name = 'login'),
    path('banchay/', core_view.banchayview, name = 'banchay'),
    path('diemcao/', core_view.diemcaoview, name = 'diemcao'),
    path('giamdan/', core_view.giamdanview, name = 'giamdan'),
    path('tangdan/', core_view.tangdanview, name = 'tangdan'),
    #path('login/', profiles_views.SiteLoginView.as_view(),name = 'login'),
    #path('register/', profiles_views.SiteRegisterView.as_view(),name = 'register'),
    #path('profile/', profiles_views.EditProfileView.as_view(),name = 'profile'),
   
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)