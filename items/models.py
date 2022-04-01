from pyexpat import model
from statistics import mode
from django.conf import settings
from django.db import models
from django.conf import settings


def company_directory_path(filename):
    return 'companies/{0}'.format(filename)


def item_directory_path(instance, filename):
    return 'items/{0}/{1}'.format(instance.name, filename)


def poster_directory_path(filename):
    return 'posters/{0}'.format(filename)


def slider_directory_path(filename):
    return 'sliders/{0}'.format(filename)


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to=company_directory_path, null=True, blank=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    name_en = models.CharField(
        max_length=100, blank=True, null=True, db_column="name_en")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    name_en = models.CharField(
        max_length=100, blank=True, null=True, db_column="name_en")
    subcategories = models.ManyToManyField(SubCategory)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    name_en = models.CharField(
        max_length=100, blank=True, null=True, db_column="name_en")

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
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategories = models.ManyToManyField(SubCategory, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    price = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    image1 = models.ImageField(
        upload_to=item_directory_path, null=True, blank=True)
    image2 = models.ImageField(
        upload_to=item_directory_path, null=True, blank=True)
    image3 = models.ImageField(
        upload_to=item_directory_path, null=True, blank=True)
    image4 = models.ImageField(
        upload_to=item_directory_path, null=True, blank=True)
    # Featured only
    is_featured = models.BooleanField(default=False)
    multiplier = models.IntegerField(default=1)
    poster = models.ImageField(
        upload_to=poster_directory_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Slider(models.Model):
    image = models.ImageField(
        upload_to=slider_directory_path, null=True, blank=True)


class Video(models.Model):
    name = models.CharField(max_length=100)
    video_url = models.CharField(max_length=200)

    def __str__(self):
        return self.name
