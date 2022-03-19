from statistics import mode
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from items.models import Item
from .managers import CustomUserManager

import random


USER_ROLES = (
    ("1", "admin"),
    ("2", "staff"),
    ("3", "customer"),
)

ORDER_STATE = (
    ("1", "is_ordered"),
    ("2", "is_payed"),
    ("3", "on_delivery"),
    ("4", "successful"),
    ("5", "unsuccessful"),
)


def create_new_ref_number():
    return "A" + str(random.randint(100000, 999999))


# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/users/<id>/<filename>
#     return 'users/{0}/{1}'.format(instance.user.id, filename)


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)


class CustomUser(AbstractUser):
    # phone_number
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(_('email address'), unique=False)

    # REQUIRED_FIELDS = []

    # objects = CustomUserManager()

    role = models.CharField(max_length=20, choices=USER_ROLES, default="3")
    company_name = models.CharField(max_length=80, null=True, blank=True)
    company_id = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    favorite = models.ManyToManyField(Item, null=True, blank=True)
    cart = models.ManyToManyField(CartItem, null=True, blank=True)
    level = models.IntegerField(default=0)
    percent = models.IntegerField(default=1)
    bonus = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.username


# class Order(models.Model):
#     ref = models.CharField(max_length=10, unique=True,
#                            default=create_new_ref_number)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     items = models.ManyToManyField(CartItem, null=True, blank=True)
#     total = models.IntegerField(default=0)
#     bonus = models.IntegerField(default=0)
#     phone_number = models.CharField(max_length=30, null=True, blank=True)
#     address = models.TextField(blank=True)
#     info = models.TextField(blank=True)
#     state = models.CharField(max_length=20, choices=ORDER_STATE, default="1")
#     created_at = models.DateTimeField(auto_now_add=True)
#     on_delivery_at = models.DateTimeField(null=True, blank=True)
#     successful_at = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return self.ref


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
