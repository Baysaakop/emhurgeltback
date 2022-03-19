from statistics import mode
from rest_framework import serializers
from django.db import transaction
from django.utils.translation import gettext as _
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.models import TokenModel

from items.serializers import ItemSerializer
from .models import CustomUser, CartItem, USER_ROLES


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'item', 'count')


class CustomUserSerializer(serializers.ModelSerializer):

    favorite = ItemSerializer(read_only=True, many=True)
    cart = CartItemSerializer(read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'company_name',
                  'company_id', 'address', 'role', 'is_confirmed',
                  'favorite', 'cart', 'level', 'percent', 'bonus', 'total']


class CustomTokenSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = TokenModel
        fields = ('key', 'user')


class CustomRegisterSerializer(RegisterSerializer):
    company_name = serializers.CharField(max_length=80, required=False)
    company_id = serializers.CharField(max_length=30, required=False)
    address = serializers.CharField(max_length=200, required=False)
    role = serializers.ChoiceField(choices=USER_ROLES)

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        if (self.data.get('role') == "1"):
            return None

        else:
            user = super().save(request)
            user.role = self.data.get('role')
            if (self.data.get('role') == "2"):
                user.is_confirmed = True
            if (self.data.get('company_name') != ""):
                user.company_name = self.data.get('company_name')
            if (self.data.get('company_id') != ""):
                user.company_id = self.data.get('company_id')
            if (self.data.get('address') != ""):
                user.address = self.data.get('address')
            user.save()
            return user


# class OrderSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     items = CartItemSerializer(read_only=True, many=True)

#     class Meta:
#         model = Order
#         fields = (
#             'id', 'ref', 'user', 'items', 'total', 'bonus', 'phone_number', 'address', 'info', 'state', 'created_at', 'on_delivery_at', 'successful_at'
#         )
