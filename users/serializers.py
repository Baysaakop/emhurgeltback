from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
from .models import Profile, CartItem, Order, City, District, Section, Building
from items.serializers import ItemSerializer


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')


class DistrictSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = District
        fields = ('id', 'city', 'name')


class SectionSerializer(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)

    class Meta:
        model = Section
        fields = ('id', 'district', 'name')


class BuildingSerializer(serializers.ModelSerializer):
    section = SectionSerializer(read_only=True)

    class Meta:
        model = Building
        fields = ('id', 'section', 'name')


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'item', 'count')


class ProfileSerializer(serializers.ModelSerializer):
    favorite = ItemSerializer(read_only=True, many=True)
    cart = CartItemSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = (
            'id', 'user', 'description', 'phone_number', 'address', 'favorite', 'cart', 'level', 'percent', 'bonus', 'total', 'birth_date', 'avatar', 'role', 'created_at', 'updated_at'
        )


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'profile'
        )


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = CartItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = (
            'id', 'ref', 'user', 'items', 'total', 'bonus', 'phone_number', 'address', 'info', 'state', 'created_at', 'on_delivery_at', 'successful_at'
        )
