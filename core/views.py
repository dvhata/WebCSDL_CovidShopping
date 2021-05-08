from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect, HttpResponse
from product.models import San_pham,Loaisp
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.functions import Length
from django.db.models import Count
from django.db.migrations import operations
from order.models import Don_dat_hang
from cart.models import gio_hang
from user.models import Khach_hang
from review.models import Nhan_xet
from order.models import Don_dat_hang
from django.contrib.auth.models import User
from user_auth.forms import RegisterForm
from django.utils import timezone
import random

# Create your views here.



class HomeVieww(View):
    def get(self, request):
        s = Don_dat_hang.objects.all()
        sp = San_pham.objects.order_by("gia")[:4]
        products = list(San_pham.objects.all())
        prod = random.sample(products, 4)
        
        return render(request,'trangChu.html', {"sp":sp ,'product': prod})

class HomeView(View):
    def get(self, request):
        s = Don_dat_hang.objects.all()
        sp = San_pham.objects.order_by("gia")[:4]
        products = list(San_pham.objects.all())
        prod = random.sample(products,4)
        return render(request,'trangChuafterlogin.html', {"sp":sp , 'product': prod})
class SanphamView(View):    
    def get(self,request):
        #Tìm spp theo thanh search trên wed
        if request.GET.get("search"):
            kw = request.GET.get("search")
            k = San_pham.objects.filter(tensp__icontains=kw)
        else:
            k = San_pham.objects.order_by("-id")
        h = k.count()
        #chia theo loại sp
        lsp = Loaisp.objects.all()
    
        #Hiển thị các phân loại
        sp = San_pham.objects.all().values('phanloai').distinct()
        sp_xuatxu = San_pham.objects.all().values('xuatxu').distinct() #Lọc theo  xuất xứ
        sp_thuonghieu = San_pham.objects.all().values('thuonghieu').distinct() #Lọc theo thương hiệu
        #them vao gio hang:
        
        #chia page
        paginator = Paginator(k,9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sanPham.html', {'page_obj': page_obj , 'h': h, 'lsp': lsp , 'sp': sp,'sp_xuatxu':sp_xuatxu,
        'sp_thuonghieu':sp_thuonghieu})

# def sanphamcutheView():


class SiteLoginView(LoginView):
    template_name = "login.html"
def register(request):
    context = {
        'form' : RegisterForm(),
        'error' : None
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username=username, password=password)
            kh = Khach_hang(user=user)
            kh.save()
            return redirect('/login')
        except Exception as e:
            context['error'] = e
            return render(request, 'login.html',context)
        return render(request, 'login.html',context)
  
    registerForm = RegisterForm() 
    return render(request, 'register.html', {'form':registerForm})

@login_required
def cart_add(request, id, url):
    userId = User.objects.get(username=request.user)
    if not userId:
        # error
        pass
    kh = Khach_hang.objects.get(user_id=userId)
    product = San_pham.objects.get(id=id)
    cart = gio_hang(khach_hang = kh , san_pham = product , so_luong=1)
    cart.save()
    return redirect(url)

@login_required()
def order_cart(request):
    userId = User.objects.get(username=request.user)
    if not userId:
        # error
        pass
    kh = Khach_hang.objects.get(user_id=userId)
    gio_hang.objects.filter(khach_hang=kh).delete()
    return render(request,'datHangThanhCong.html')

@login_required
def cart_clear(request):
    userId = User.objects.get(username=request.user)
    if not userId:
        # error
        pass
    kh = Khach_hang.objects.get(user_id=userId)
    gio_hang.objects.filter(khach_hang=kh).delete()
    return redirect("giohang")


@login_required
def giohangview(request):
    context = {
        'items': []
    }
    userId = User.objects.get(username=request.user)
    if not userId:
        # error
        pass
    kh = Khach_hang.objects.get(user_id=userId)
    cart = gio_hang.objects.filter(khach_hang=kh)

    for each in cart:
        spId = each.san_pham_id
        sp = San_pham.objects.get(id=spId)
        sl = each.so_luong
        context['items'].append({
            'san_pham' : sp,
            'so_luong' : sl
        })
    if cart:
        don = Don_dat_hang(khach_hang=kh,san_pham=sp,so_luong=1,ngay_dat=timezone.now()
        ,ngay_giao=timezone.now(),tinh_trang='đã đặt',hinh_thuc_thanh_toan='thanh toán khi nhận hàng')
        don.save()
    return render(request, 'giohang.html', context=context)

def userview(request):
    userId = User.objects.get(username=request.user)
    kh = Khach_hang.objects.get(user_id=userId)
    return render(request, 'user.html',{'kh':kh, 'user': userId})
#san phẩm cụ thể
class Index(View):
    def get(self,request,sanpham_id):
        k = San_pham.objects.get(pk = sanpham_id)
        nx = Nhan_xet.objects.filter(san_pham=k)
        return render(request, 'sanPhamCuThe.html', {'sanpham':k, 'nx':nx})  


#lọc theo loại sp
def loaispview(request, loaisp_id):
    #tìm kiếm
    if request.GET.get("search"):
        kw = request.GET.get("search")
        k = San_pham.objects.filter(tensp__icontains=kw)
    else:
        k = San_pham.objects.order_by("-id")
    k = k.filter(loaisp = Loaisp.objects.get(pk = loaisp_id) ) # Tìm sp có cùng loại sp
    h = k.count()
    lsp = Loaisp.objects.all() #in ra các loại sp
    sp = San_pham.objects.all().values('phanloai').distinct() #Lọc theo chủng loại
    sp_xuatxu = San_pham.objects.all().values('xuatxu').distinct() #Lọc theo  xuất xứ
    sp_thuonghieu = San_pham.objects.all().values('thuonghieu').distinct() #Lọc theo thương hiệu
    #chia page
    paginator = Paginator(k,9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "sanPham.html", {"page_obj":page_obj ,'sanpham' : k ,'h': h, 'lsp': lsp , 'sp': sp ,'sp_xuatxu':sp_xuatxu, 
    'sp_thuonghieu':sp_thuonghieu})


def banchayview(request):
    if request.GET.get("search"):
        kw = request.GET.get("search")
        k = San_pham.objects.filter(tensp__icontains=kw)
    else:
        k = San_pham.objects.order_by("-id")
    h = k.count()
    lsp = Loaisp.objects.all() #in ra các loại sp
    sp = San_pham.objects.all().values('phanloai').distinct() #Lọc theo chủng loại
    sp_xuatxu = San_pham.objects.all().values('xuatxu').distinct() #Lọc theo  xuất xứ
    sp_thuonghieu = San_pham.objects.all().values('thuonghieu').distinct() #Lọc theo thương hiệu
    
    # thử làm bán chạy
    context = {
        'items': [],
        'sanpham' : k,
        'h': h,
        'lsp': lsp ,
        'sp': sp ,
        'sp_xuatxu' : sp_xuatxu, 
        'sp_thuonghieu' : sp_thuonghieu,
    }
    don= Don_dat_hang.objects.values('san_pham').annotate(dcount = Count('san_pham')).order_by()
    for each in don:
        spId = each['san_pham']
        sp = San_pham.objects.get(id=spId)
        context['items'].append({
            'san_pham' : sp
        })
    paginator = Paginator(k,9)
    page_number = request.GET.get('page')
    context['page_obj'] = paginator.get_page(page_number)
    
    return render(request, "sanPhamBanChayNhat.html", context=context)

def diemcaoview(request):
    if request.GET.get("search"):
        kw = request.GET.get("search")
        k = San_pham.objects.filter(tensp__icontains=kw)
    else:
        k = San_pham.objects.order_by("-id")
        h = k.count()
        #chia theo loại sp
        lsp = Loaisp.objects.all()
    
        #Hiển thị các phân loại
        sp = San_pham.objects.all().values('phanloai').distinct()
        sp_xuatxu = San_pham.objects.all().values('xuatxu').distinct() #Lọc theo  xuất xứ
        sp_thuonghieu = San_pham.objects.all().values('thuonghieu').distinct() #Lọc theo thương hiệu
        #chia page
        paginator = Paginator(k,9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sanPhamDiemCaoNhat.html', {'page_obj': page_obj , 'h': h, 'lsp': lsp , 'sp': sp,'sp_xuatxu':sp_xuatxu,
        'sp_thuonghieu':sp_thuonghieu})

def giamdanview(request):
    if request.GET.get("search"):
        kw = request.GET.get("search")
        k = San_pham.objects.filter(tensp__icontains=kw)
    else:
        k = San_pham.objects.order_by("-id")
    k = k.order_by("-gia")
    h = k.count()
    lsp = Loaisp.objects.all() #in ra các loại sp
    sp = San_pham.objects.all().values('phanloai').distinct() #Lọc theo chủng loại
    sp_xuatxu = San_pham.objects.all().values('xuatxu').distinct() #Lọc theo  xuất xứ
    sp_thuonghieu = San_pham.objects.all().values('thuonghieu').distinct() #Lọc theo thương hiệu
    #chia page
    #chia page
    paginator = Paginator(k,9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "sanPhamGiaCaoDenThap.html", {"page_obj":page_obj ,'sanpham' : k ,'h': h, 'lsp': lsp , 'sp': sp ,'sp_xuatxu':sp_xuatxu, 
    'sp_thuonghieu':sp_thuonghieu})

def tangdanview(request):
    if request.GET.get("search"):
        kw = request.GET.get("search")
        k = San_pham.objects.filter(tensp__icontains=kw)
    else:
        k = San_pham.objects.order_by("-id")
    k = k.order_by("gia")
    h = k.count()
    lsp = Loaisp.objects.all() #in ra các loại sp
    sp = San_pham.objects.all().values('phanloai').distinct() #Lọc theo chủng loại
    sp_xuatxu = San_pham.objects.all().values('xuatxu').distinct() #Lọc theo  xuất xứ
    sp_thuonghieu = San_pham.objects.all().values('thuonghieu').distinct() #Lọc theo thương hiệu
    #chia page
    #chia page
    paginator = Paginator(k,9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "sanPhamGiaThapDenCao.html", {"page_obj":page_obj ,'sanpham' : k ,'h': h, 'lsp': lsp , 'sp': sp,'sp_xuatxu':sp_xuatxu, 
    'sp_thuonghieu':sp_thuonghieu})