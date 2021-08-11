from re import T
from django.db import models
from django.contrib.auth.models import User
from django.db.models.expressions import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from items.models import Item
from addresses.models import Address
import random

USER_ROLES = (
    ("1", "admin"),
    ("2", "moderator"),
    ("3", "user"),
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


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<id>/<filename>
    return 'users/{0}/{1}'.format(instance.user.id, filename)


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True)
    favorite = models.ManyToManyField(Item, null=True, blank=True)
    cart = models.ManyToManyField(CartItem, null=True, blank=True)
    point = models.IntegerField(default=2)
    bonus = models.IntegerField(default=0)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True)
    role = models.CharField(max_length=20, choices=USER_ROLES, default="3")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    ref = models.CharField(max_length=10, unique=True,
                           default=create_new_ref_number)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, null=True, blank=True)
    total = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField(blank=True)
    info = models.TextField(blank=True)
    state = models.CharField(max_length=20, choices=ORDER_STATE, default="1")
    created_at = models.DateTimeField(auto_now_add=True)
    on_delivery_at = models.DateTimeField(null=True, blank=True)
    successful_at = models.DateTimeField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
