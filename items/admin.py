from django.contrib import admin
from .models import Company, Type, Category, SubCategory, Tag, Item

admin.site.register(Company)
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Tag)
admin.site.register(Item)
