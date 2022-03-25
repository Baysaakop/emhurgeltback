from unicodedata import category
from rest_framework import serializers
from .models import Company, Category, SubCategory, Tag, Item, Slider, Video


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'image')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'name_en')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'name_en', 'subcategories')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'name_en')


class ItemSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategories = SubCategorySerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'name_en', 'description', 'description_en', 'ingredients', 'ingredients_en', 'usage', 'usage_en', 'caution', 'caution_en', 'storage', 'storage_en',
                  'company', 'category', 'subcategories', 'tags', 'price', 'count', 'is_featured', 'multiplier', 'image1', 'image2', 'image3', 'image4', 'poster', 'created_at', 'updated_at')


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ('id', 'image')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'name', 'video_url')
