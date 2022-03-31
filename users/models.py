from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from items.models import Item

import random


USER_ROLES = (
    ("1", "admin"),
    ("2", "staff"),
    ("3", "customer"),
)


def create_new_ref_number():
    return "A" + str(random.randint(1000000, 9999999))


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)


class CustomUser(AbstractUser):
    # phone_number
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(
        _('email address'), unique=True)

    # REQUIRED_FIELDS = []

    # objects = CustomUserManager()

    role = models.CharField(max_length=20, choices=USER_ROLES, default="3")
    company_name = models.CharField(max_length=80, null=True, blank=True)
    company_id = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    favorite = models.ManyToManyField(Item, null=True, blank=True)
    cart = models.ManyToManyField(CartItem, null=True, blank=True)
    level = models.IntegerField(default=1)
    bonus = models.IntegerField(default=1000)
    total = models.IntegerField(default=0)
    bonus_collected = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Order(models.Model):
    ref = models.CharField(max_length=10, unique=True,
                           default=create_new_ref_number)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, null=True, blank=True)
    total = models.IntegerField(default=0)
    bonus_used = models.IntegerField(default=0)
    bonus_granted = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField(blank=True)
    is_delivered = models.BooleanField(default=False)
    is_payed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ref
