from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from addresses.models import Address


def company_directory_path(instance, filename):
    return 'companies/{0}/{1}'.format(instance.id, filename)


def item_directory_path(instance, filename):
    return 'items/{0}/{1}'.format(instance.id, filename)


def shop_directory_path(instance, filename):
    return 'shops/{0}/{1}'.format(instance.id, filename)


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to=company_directory_path, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(
        upload_to=shop_directory_path, null=True, blank=True)

    def __str__(self):
        return self.name


class ItemImage(models.Model):
    image = models.ImageField(
        upload_to=item_directory_path, null=True, blank=True)


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    ingredients = models.TextField(blank=True, null=True)
    usage = models.TextField(blank=True, null=True)
    caution = models.TextField(blank=True, null=True)
    storage = models.TextField(blank=True, null=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ManyToManyField(Category, null=True, blank=True)
    tag = models.ManyToManyField(Tag, null=True, blank=True)
    price = models.IntegerField(default=0)
    shops = models.ManyToManyField(Shop, null=True, blank=True)
    rating = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    is_brand = models.BooleanField(default=False)
    images = models.ManyToManyField(ItemImage, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="item_created_by")
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="item_updated_by")

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    thumbnail = models.ImageField(
        upload_to='posts/%Y/%m/%d', null=True, blank=True)
    video = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="post_created_by")

    def __str__(self):
        return self.title
