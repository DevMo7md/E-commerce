from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

class OrderItemInLine(admin.StackedInline):
    model = OrderItem
    extra = 0

# Extend user model
class OrderAdmin(admin.ModelAdmin):
    
    model = Order
    readonly_fields = ["date_ordered"]
    inlines = [OrderItemInLine]

admin.site.unregister(Order)

admin.site.register(Order, OrderAdmin)
    