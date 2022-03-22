from rest_framework import serializers
from .models import Company, Type, Category, SubCategory, Tag, Item, Slider


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


class ItemSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    types = TypeSerializer(read_only=True, many=True)
    categories = CategorySerializer(read_only=True, many=True)
    subcategories = SubCategorySerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'name_en', 'description', 'description_en', 'ingredients', 'ingredients_en', 'usage', 'usage_en', 'caution', 'caution_en', 'storage', 'storage_en',
                  'company', 'types', 'categories', 'subcategories', 'tags', 'price', 'count', 'is_featured', 'multiplier', 'video', 'image1', 'image2', 'image3', 'image4', 'poster', 'created_at', 'updated_at')


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ('id', 'image')
