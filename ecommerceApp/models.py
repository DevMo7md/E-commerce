from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True) 
    address2 = models.CharField(max_length=200, blank=True) 
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True) 
    country = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=2000, null=True)

    def __str__(self) :
        return self.user.username
    

# create user profile by defult when user signed up

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

# automate the profile things
post_save.connect(create_profile, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) :
        return self.name

class Customer(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=50)

    def __str__(self) :
        return f'{self.first_name} {self.last_name}'

class Product(models.Model):

    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    about_product = models.CharField(max_length=300,null=True, blank=True )
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/products/', null=True, blank=True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    


    def __str__(self) :
        return self.name


class Order(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True, null=True)
    phone = models.CharField(max_length=15, default='', blank=True, null=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)


    def __str__(self) :
        return str(self.product)