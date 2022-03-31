from re import search
from django.contrib import admin
from django.contrib.sites.models import Site
from .models import CartItem, CustomUser, Order


class CustomUserAdminModel(admin.ModelAdmin):
    search_fields = ('username', 'company_name', 'company_id',)


class OrderAdminModel(admin.ModelAdmin):
    search_fields = ('ref', 'customer__username', 'phone_number',)


admin.site.register(CartItem)
admin.site.register(CustomUser, CustomUserAdminModel)
admin.site.register(Order, OrderAdminModel)

admin.site.unregister(Site)


class SiteAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'domain')
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'domain')
    list_display_links = ('name',)
    search_fields = ('name', 'domain')


admin.site.register(Site, SiteAdmin)
