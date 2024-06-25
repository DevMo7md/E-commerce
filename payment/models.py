from django.db import models
from django.contrib.auth.models import User
from ecommerceApp.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_full_name = models.CharField(max_length=255, null=True, blank=True)
    shipping_email = models.EmailField()
    shipping_phone = models.CharField(max_length=15, null=True, blank=True)
    shipping_address1 = models.CharField(max_length=255, null=True, blank=True)
    shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_country = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=255, null=True, blank=True)
    shipping_state = models.CharField(max_length=255, null=True, blank=True)

    class Meta :
        verbose_name_plural = "Shiping Address"

    def __str__(self):
        return f'Shipping address - {str(self.id)}'    
    

def create_shippingAddress(sender, instance, created, **kwargs):
    if created:
        user_shippingAddress = ShippingAddress(user=instance)
        user_shippingAddress.save()

# automate the shipping_adress things
post_save.connect(create_shippingAddress, sender=User)    



# create order model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField()
    shipping_address = models.TextField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=15, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1 ,null=True, blank=True)
    date_shipped = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Order - {str(self.id)}'
    
@receiver(pre_save, sender=Order)    
def set_shipping_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        opj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not opj.shipped:
            instance.date_shipped = now
    
# create order items model

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')# دا المستخدم في ارسال الايميل الريليتد نيم دا
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.BigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f'Order item - {str(self.id)}'