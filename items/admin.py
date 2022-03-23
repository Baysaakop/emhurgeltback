from django.contrib import admin
from .models import Company, Type, Category, SubCategory, Tag, Item, Slider, Video


class ItemAdminModel(admin.ModelAdmin):
    search_fields = ('name',)


class CompanyAdminModel(admin.ModelAdmin):
    search_fields = ('name',)


class CategoryAdminModel(admin.ModelAdmin):
    search_fields = ('name',)


class SubCategoryAdminModel(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(Company, CompanyAdminModel)
admin.site.register(Type)
admin.site.register(Category, CategoryAdminModel)
admin.site.register(SubCategory, SubCategoryAdminModel)
admin.site.register(Tag)
admin.site.register(Item, ItemAdminModel)
admin.site.register(Slider)
admin.site.register(Video)
