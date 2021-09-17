from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Company, Type, Category, SubCategory, Tag, Shop, Item, Post


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'image')


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'name', 'name_en', 'description')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'type', 'name', 'name_en', 'description')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'name', 'name_en', 'description')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'name_en', 'description')


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'phone_number', 'address', 'image')


class ItemSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    types = TypeSerializer(read_only=True, many=True)
    categories = CategorySerializer(read_only=True, many=True)
    subcategories = SubCategorySerializer(read_only=True, many=True)
    tag = TagSerializer(read_only=True, many=True)
    shops = ShopSerializer(read_only=True, many=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'name_en', 'description', 'description_en', 'ingredients', 'ingredients_en', 'usage', 'usage_en', 'caution', 'caution_en', 'storage', 'storage_en',
                  'company', 'types', 'categories', 'subcategories', 'tags', 'price', 'shops', 'rating', 'count', 'is_featured', 'video', 'image1', 'image2', 'image3', 'image4', 'poster', 'created_by', 'updated_by', 'created_at', 'updated_at')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id', 'title', 'content', 'thumbnail', 'video', 'created_at', 'created_by'
        )
