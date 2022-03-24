from django.contrib import admin
from .models import Company, Category, SubCategory, Tag, Item, Slider, Video


class ItemAdminModel(admin.ModelAdmin):
    search_fields = ('name',)


class CompanyAdminModel(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(Company, CompanyAdminModel)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Tag)
admin.site.register(Item, ItemAdminModel)
admin.site.register(Slider)
admin.site.register(Video)
