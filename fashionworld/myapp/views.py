from django.shortcuts import render,redirect
from myapp.models import *
from django.views.generic import TemplateView,CreateView,View,UpdateView,DetailView,ListView
from myapp.forms import *
from django.urls import reverse,reverse_lazy
# Create your views here.

def home(request):
    data=Product.objects.all().order_by('-id')
    return render(request,'myapp/index.html',{'data':data})


def category(request):
    category=Category.objects.all().order_by('-id')
    return render(request,'myapp/category.html',{"category":category})

def brand(request):
    brand=Brand.objects.all().order_by('-id')
    return render(request,'myapp/brand.html',{"brand":brand})

def category_product(request,cat_id):
    category=Category.objects.get(id=cat_id)
    data=Product.objects.filter(category=category).order_by('-id')
    return render(request,'myapp/cat_product.html',{'data':data,'category':category})

def brand_product(request,brand_id):
    brand=Brand.objects.get(id=brand_id)
    data=Product.objects.filter(brand=brand)
    return render(request,'myapp/brand_product.html',{'data':data,'brand':brand})

def product_detail(request,id):
    product=Product.objects.get(id=id)
    product.viewcount+=1
    related=Product.objects.filter(category=product.category).exclude(id=id)[:4]
    return render(request,'myapp/product_detail.html',{'product':product,'related':related})


class Add_Cart(TemplateView):
    template_name="myapp/cart_add.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        product_id=self.kwargs['pro_id']
        product_obj=Product.objects.get(id=product_id)
        cart_id=self.request.session.get('cart_id',None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            this_product_in_cart=cart_obj.cartproduct_set.filter(product=product_obj)
            if this_product_in_cart.exists():
                cartproduct=this_product_in_cart.last()
                cartproduct.quantity+=1
                cartproduct.subtotal+=product_obj.sell_price
                cartproduct.save()
                cart_obj.total+=product_obj.sell_price
                cart_obj.save()
            else:
                cartproduct=CartProduct.objects.create(cart=cart_obj,product=product_obj,rate=product_obj.sell_price,quantity=1,subtotal=product_obj.sell_price)
                cart_obj.total+=product_obj.sell_price
                cart_obj.save()
        else:
            cart_obj=Cart.objects.create(total=0)
            self.request.session['cart_id']=cart_obj.id
            cartproduct=CartProduct.objects.create(cart=cart_obj,product=product_obj,rate=product_obj.sell_price,quantity=1,subtotal=product_obj.sell_price)
            cart_obj.total+=product_obj.sell_price
            cart_obj.save()
        return context

class MyCartView(TemplateView):
    template_name='myapp/mycart.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        cart_id=self.request.session.get('cart_id',None)
        if cart_id:
            cart=Cart.objects.get(id=cart_id)
        else:
            cart=None
        context['cart']=cart
        return context

class ManageCartView(View):
    def get(self,request,*args,**kwargs):
        cp_id=self.kwargs['cp_id']
        action=request.GET.get("action")
        cp_obj=CartProduct.objects.get(id=cp_id)
        cart_obj=cp_obj.cart
        if action=='inc':
            cp_obj.quantity+=1
            cp_obj.subtotal+=cp_obj.rate
            cp_obj.save()
            cart_obj.total+=cp_obj.rate
            cart_obj.save()
        elif action=='dec':
            cp_obj.quantity-=1
            cp_obj.subtotal-=cp_obj.rate
            cp_obj.save()
            cart_obj.total-=cp_obj.rate
            cart_obj.save()
            if(cp_obj.quantity==0):
                cp_obj.delete()
        elif action=='rmv':
            cart_obj.total-=cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect('mycart')


class EmptyCart(View):
    def get(self,request,*args,**kwargs):
        cart_id=request.session.get("cart_id",None)
        if cart_id:
            cart=Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total=0
            cart.save()
        return redirect('mycart')



class CheckoutView(CreateView):
    template_name='myapp/checkout.html'
    form_class=CheckoutForm
    success_url=reverse_lazy('home')

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        cart_id=self.request.session.get("cart_id",None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
        else:
            cart_obj=None
        context['cart']=cart_obj
        return context

    def form_valid(self,form):
        cart_id=self.request.session.get("cart_id",None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            form.instance.cart=cart_obj
            form.instance.subtotal=cart_obj.total
            form.instance.discount=0
            form.instance.total=cart_obj.total
            form.instance.order_status="Order Received"
            del self.request.session["cart_id"]
        else:
            return redirect('home')
        return super().form_valid(form)
