from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Company, Category, Tag, Shop, Item, ItemImage, Post
from addresses.serializers import AddressSerializer


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'image')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'description')


class ShopSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Shop
        fields = ('id', 'name', 'phone_number', 'address', 'image')


class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ('id', 'image')


class ItemSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    category = CategorySerializer(read_only=True, many=True)
    tag = TagSerializer(read_only=True, many=True)
    images = ItemImageSerializer(read_only=True, many=True)
    shops = ShopSerializer(read_only=True, many=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'ingredients', 'usage', 'caution',
                  'company', 'category', 'tag', 'price', 'shops', 'rating', 'total', 'is_brand', 'images', 'created_by', 'updated_by', 'created_at', 'updated_at')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id', 'title', 'content', 'thumbnail', 'video', 'created_at', 'created_by'
        )
