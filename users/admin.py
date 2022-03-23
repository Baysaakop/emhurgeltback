from re import search
from django.contrib import admin
from .models import CartItem, CustomUser, Order


class CustomUserAdminModel(admin.ModelAdmin):
    search_fields = ('username', 'company_name', 'company_id',)


class OrderAdminModel(admin.ModelAdmin):
    search_fields = ('ref', 'customer__username', 'phone_number',)


admin.site.register(CartItem)
admin.site.register(CustomUser, CustomUserAdminModel)
admin.site.register(Order, OrderAdminModel)
