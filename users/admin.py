from django.contrib import admin
from .models import CartItem, CustomUser, Order

admin.site.register(CartItem)
admin.site.register(CustomUser)
admin.site.register(Order)
