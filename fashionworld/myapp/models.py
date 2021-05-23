from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=264)
    address=models.TextField()
    join_on=models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    title=models.CharField(max_length=264)
    image=models.ImageField(upload_to="cat_pics")

    def __str__(self):
        return self.title

class Brand(models.Model):
    title=models.CharField(max_length=264)
    image=models.ImageField(upload_to="brand_pics")

    def __str__(self):
        return self.title

class Product(models.Model):
    title=models.CharField(max_length=264)
    image=models.ImageField(upload_to="product_pics")
    slug=models.SlugField()
    detail=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    mark_price=models.PositiveIntegerField()
    sell_price=models.PositiveIntegerField()
    warranty=models.CharField(max_length=264)
    return_policy=models.CharField(max_length=264)
    viewcount=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Cart(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True,null=True)
    total=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "cart "+str(self.id)

class CartProduct(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    rate=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField()
    subtotal=models.PositiveIntegerField()

    def __str__(self):
        return "cart"+str(self.cart.id)
ORDER_STATUS=(
('order received','Order Received'),
('Order Completed','Order Completed'),
('Order Cancelled','Order Cancelled'),
)
class Order(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    order_by=models.CharField(max_length=264)
    ship_address=models.TextField()
    mobile=models.PositiveIntegerField()
    email=models.EmailField()
    subtotal=models.PositiveIntegerField()
    discount=models.PositiveIntegerField()
    total=models.PositiveIntegerField()
    order_status=models.CharField(max_length=264,choices=ORDER_STATUS)
    created_at=models.DateTimeField(auto_now_add=True)
