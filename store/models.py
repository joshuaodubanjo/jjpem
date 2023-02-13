from django.db import models
from uuid import uuid4

from django.contrib.auth.models import AbstractUser,AbstractBaseUser

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class User(AbstractUser):     
    email = models.EmailField(unique=True) 

class Customer(models.Model):
    Gold = 'Gold'
    Silver = 'Silver'
    Bronze = 'Bronze'
    MEMBERSHIP_OPTIONS = [
        (Gold, 'Gold'),
        (Silver, 'Silver'),
        (Bronze, 'Bronze')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=50)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=50, choices=MEMBERSHIP_OPTIONS,default=Silver)

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['first_name', 'last_name']) 
    #     ]

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_customer_for_user(sender, instance,created, **kwargs):
    if created:
        Customer.objects.create(user=instance)             
    
class Address(models.Model):
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=70)
    state = models.CharField(max_length=30)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE,primary_key=True)

class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
    
class Promotion(models.Model):
    title = models.CharField(max_length=200)


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(default='-', null=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    junk = models.CharField(max_length=250, blank=True, null=True)
    when_uploaded = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    promotions = models.ManyToManyField(Promotion)

    def __str__(self):
        return self.title


class ProductImage(models.Model):     
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='images')     
    image = models.ImageField(upload_to='store/images')

class Review(models.Model):     
    product = models.ForeignKey(Product, on_delete=models.CASCADE)     
    reviewer_name = models.CharField(max_length=250)     
    remark = models.TextField()     
    posted_at = models.DateField(auto_now_add=True) 
     
    def __str__(self):         
        return f'Review for {self.product.title}'        
    
    
class Order(models.Model):
    PAYMENT_STATUS =[
        ('pending','pending'),
        ('completed','completed'),
        ('failed','failed')
    ]

    DELIVERY_STATUS =[
        ('pending','pending'),
        ('completed','completed'),
        ('failed','failed')
    ]

    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=50,choices=PAYMENT_STATUS, default='pending')
    delivery_status = models.CharField(max_length=50, choices=DELIVERY_STATUS, default='pending')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    placed_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.PositiveSmallIntegerField()

    class Meta:         
        unique_together = [['cart','product']]
