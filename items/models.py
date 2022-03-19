from django.conf import settings
from django.db import models
from django.conf import settings


def company_directory_path(instance, filename):
    return 'companies/{0}/{1}'.format(instance.id, filename)


def item_directory_path(instance, filename):
    return 'items/{0}/{1}'.format(instance.id, filename)


def poster_directory_path(instance, filename):
    return 'posters/{0}/{1}'.format(instance.id, filename)


def shop_directory_path(instance, filename):
    return 'shops/{0}/{1}'.format(instance.id, filename)


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to=company_directory_path, null=True, blank=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=100)
    name_en = models.CharField(
        max_length=100, blank=True, null=True, db_column="name_en")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    type = models.ForeignKey(
        Type, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    name_en = models.CharField(
        max_length=100, blank=True, null=True, db_column="name_en")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    name_en = models.CharField(
        max_length=100, blank=True, null=True, db_column="name_en")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    name_en = models.CharField(
        max_length=100, blank=True, null=True, db_column="name_en")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    name_en = models.CharField(
        max_length=100, blank=True, null=True, db_column="name_en")
    description = models.TextField(blank=True, null=True)
    description_en = models.TextField(
        blank=True, null=True, db_column="description_en")
    ingredients = models.TextField(blank=True, null=True)
    ingredients_en = models.TextField(
        blank=True, null=True, db_column="ingredients_en")
    usage = models.TextField(blank=True, null=True)
    usage_en = models.TextField(blank=True, null=True, db_column="usage_en")
    caution = models.TextField(blank=True, null=True)
    caution_en = models.TextField(
        blank=True, null=True, db_column="caution_en")
    storage = models.TextField(blank=True, null=True)
    storage_en = models.TextField(
        blank=True, null=True, db_column="storage_en")
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True)
    types = models.ManyToManyField(Type, null=True, blank=True)
    categories = models.ManyToManyField(Category, null=True, blank=True)
    subcategories = models.ManyToManyField(SubCategory, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    price = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    video = models.CharField(max_length=200, null=True, blank=True)
    image1 = models.ImageField(
        upload_to=item_directory_path, null=True, blank=True)
    image2 = models.ImageField(
        upload_to=item_directory_path, null=True, blank=True)
    image3 = models.ImageField(
        upload_to=item_directory_path, null=True, blank=True)
    image4 = models.ImageField(
        upload_to=item_directory_path, null=True, blank=True)
    poster = models.ImageField(
        upload_to=poster_directory_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
