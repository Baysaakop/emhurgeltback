from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
from .models import Profile, CartItem, Order
from items.serializers import ItemSerializer
from addresses.serializers import AddressSerializer

class CartItemSerializer(serializers.ModelSerializer):    
    item = ItemSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ('id', 'item', 'count')    

class ProfileSerializer(serializers.ModelSerializer):    
    address = AddressSerializer(read_only=True)
    favorite = ItemSerializer(read_only=True, many=True)
    cart = CartItemSerializer(read_only=True, many=True)
    class Meta:
        model = Profile
        fields = (
            'id', 'user', 'description', 'phone_number', 'address', 'favorite', 'cart', 'point', 'bonus', 'birth_date', 'avatar', 'role', 'created_at', 'updated_at'
        )
     
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'profile'
        )

class OrderSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Order
        fields = (
            'id', 'user', 'items', 'total', 'state', 'created_at', 'confirmed_at'
        )