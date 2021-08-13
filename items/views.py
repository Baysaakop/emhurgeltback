import json
from django.db.models.fields.files import ImageField
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser
from .models import Company, Category, Shop, Tag, Item, Post
from .serializers import CompanySerializer, CategorySerializer, ShopSerializer, TagSerializer, ItemSerializer, PostSerializer
from rest_framework import viewsets, filters
from addresses.models import Address, City, District


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by('id')

    def create(self, request, *args, **kwargs):
        company = Company.objects.create(
            name=request.data['name']
        )
        if 'description' in request.data:
            company.description = request.data['description']
        if 'image' in request.data:
            company.image = request.data['image']
        company.save()
        serializer = CompanySerializer(company)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        company = self.get_object()
        if 'name' in request.data:
            company.name = request.data['name']
        if 'description' in request.data:
            company.description = request.data['description']
        if 'image' in request.data:
            company.image = request.data['image']
        company.save()
        serializer = CompanySerializer(company)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('id')


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all().order_by('id')


class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all().order_by('id')

    def create(self, request, *args, **kwargs):
        shop = Shop.objects.create(
            name=request.data['name']
        )
        if 'phone_number' in request.data:
            shop.phone_number = request.data['phone_number']
        if 'address' in request.data:
            address, created = Address.objects.get_or_create(
                city=City.objects.get(id=int(request.data['city'])),
                district=District.objects.get(
                    id=int(request.data['district'])),
                section=request.data['section'],
                address=request.data['address']
            )
            shop.address = address
        if 'image' in request.data:
            shop.image = request.data['image']
        shop.save()
        serializer = ShopSerializer(shop)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        shop = self.get_object()
        if 'name' in request.data:
            shop.name = request.data['name']
        if 'phone_number' in request.data:
            shop.phone_number = request.data['phone_number']
        if 'address' in request.data:
            address, created = Address.objects.get_or_create(
                city=City.objects.get(id=int(request.data['city'])),
                district=District.objects.get(
                    id=int(request.data['district'])),
                section=request.data['section'],
                address=request.data['address']
            )
            shop.address = address
        if 'image' in request.data:
            shop.image = request.data['image']
        shop.save()
        serializer = ShopSerializer(shop)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all().order_by('-is_brand', '-created_at')

    def get_queryset(self):
        queryset = Item.objects.all().order_by('-is_brand', '-created_at')
        name = self.request.query_params.get('name', None)
        is_brand = self.request.query_params.get('is_brand', None)
        category = self.request.query_params.get('category', None)
        tags = self.request.query_params.get('tags', None)
        pricelow = self.request.query_params.get('pricelow', None)
        pricehigh = self.request.query_params.get('pricehigh', None)
        order = self.request.query_params.get('order', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name).distinct()
            # queryset = queryset.filter(Q(name__icontains=name) | Q(tag__name=name)).distinct()
        if is_brand is not None:
            queryset = queryset.filter(is_brand=True).distinct()
        if category is not None:
            queryset = queryset.filter(category__id=category).distinct()
        if tags is not None:
            for tag in tags.split(","):
                queryset = queryset.filter(tag__id=tag).distinct()
        if pricelow is not None:
            queryset = queryset.filter(price__gte=pricelow).distinct()
        if pricehigh is not None:
            queryset = queryset.filter(price__lt=pricehigh).distinct()
        if order is not None:
            queryset = queryset.order_by('-is_brand', order)
        return queryset

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        item = Item.objects.create(
            name=request.data['name'],
            created_by=user
        )
        if 'name_en' in request.data:
            item.name_en = request.data['name_en']
        if 'description' in request.data:
            item.description = request.data['description']
        if 'description_en' in request.data:
            item.description_en = request.data['description_en']
        if 'ingredients' in request.data:
            item.ingredients = request.data['ingredients']
        if 'ingredients_en' in request.data:
            item.ingredients_en = request.data['ingredients_en']
        if 'usage' in request.data:
            item.usage = request.data['usage']
        if 'usage_en' in request.data:
            item.usage_en = request.data['usage_en']
        if 'caution' in request.data:
            item.caution = request.data['caution']
        if 'caution_en' in request.data:
            item.caution_en = request.data['caution_en']
        if 'storage' in request.data:
            item.storage = request.data['storage']
        if 'storage_en' in request.data:
            item.storage_en = request.data['storage_en']
        if 'price' in request.data:
            item.price = request.data['price']
        if 'is_brand' in request.data:
            if request.data['is_brand'] == 'true':
                item.is_brand = True
            else:
                item.is_brand = False
        if 'company' in request.data:
            item.company = Company.objects.filter(
                id=int(request.data['company']))[0]
        if 'category' in request.data:
            categories = request.data['category'].split(',')
            for cat in categories:
                item.category.add(Category.objects.filter(id=int(cat))[0])
        if 'tag' in request.data:
            tags = request.data['tag'].split(',')
            for tag in tags:
                item.tag.add(Tag.objects.filter(id=int(tag))[0])
        if 'shop' in request.data:
            shops = request.data['shop'].split(',')
            for shop in shops:
                item.shops.add(Shop.objects.filter(id=int(shop))[0])
        if 'image1' in request.data:
            item.image1 = request.data['image1']
        if 'image2' in request.data:
            item.image2 = request.data['image2']
        if 'image3' in request.data:
            item.image3 = request.data['image3']
        if 'image4' in request.data:
            item.image4 = request.data['image4']
        if 'poster' in request.data:
            item.poster = request.data['poster']
        item.save()
        serializer = ItemSerializer(item)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        item = self.get_object()
        user = Token.objects.get(key=request.data['token']).user
        item.updated_by = user
        if 'name' in request.data:
            item.name = request.data['name']
        if 'name_en' in request.data:
            item.name_en = request.data['name_en']
        if 'description' in request.data:
            item.description = request.data['description']
        if 'description_en' in request.data:
            item.description_en = request.data['description_en']
        if 'ingredients' in request.data:
            item.ingredients = request.data['ingredients']
        if 'ingredients_en' in request.data:
            item.ingredients_en = request.data['ingredients_en']
        if 'usage' in request.data:
            item.usage = request.data['usage']
        if 'usage_en' in request.data:
            item.usage_en = request.data['usage_en']
        if 'caution' in request.data:
            item.caution = request.data['caution']
        if 'caution_en' in request.data:
            item.caution_en = request.data['caution_en']
        if 'storage' in request.data:
            item.storage = request.data['storage']
        if 'storage_en' in request.data:
            item.storage_en = request.data['storage_en']
        if 'price' in request.data:
            item.price = request.data['price']
        if 'is_brand' in request.data:
            if request.data['is_brand'] == 'true':
                item.is_brand = True
            else:
                item.is_brand = False
        if 'company' in request.data:
            item.company = Company.objects.filter(
                id=int(request.data['company']))[0]
        if 'category' in request.data:
            categories = request.data['category'].split(',')
            item.category.clear()
            for cat in categories:
                item.category.add(Category.objects.filter(id=int(cat))[0])
        if 'tag' in request.data:
            tags = request.data['tag'].split(',')
            item.tag.clear()
            for tag in tags:
                item.tag.add(Tag.objects.filter(id=int(tag))[0])
        if 'shop' in request.data:
            shops = request.data['shop'].split(',')
            for shop in shops:
                item.shops.add(Shop.objects.filter(id=int(shop))[0])
        if 'image1' in request.data:
            item.image1 = request.data['image1']
        if 'image2' in request.data:
            item.image2 = request.data['image2']
        if 'image3' in request.data:
            item.image3 = request.data['image3']
        if 'image4' in request.data:
            item.image4 = request.data['image4']
        if 'poster' in request.data:
            item.poster = request.data['poster']
        item.save()
        serializer = ItemSerializer(item)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.order_by('-created_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        post = Post.objects.create(
            title=request.data['title'],
            created_by=user
        )
        if 'content' in request.data:
            post.content = request.data['content']
        if 'thumbnail' in request.data:
            post.thumbnail = request.data['thumbnail']
        post.save()
        serializer = PostSerializer(post)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        user = Token.objects.get(key=request.data['token']).user
        post.updated_by = user
        if 'title' in request.data:
            post.title = request.data['title']
        if 'content' in request.data:
            post.content = request.data['content']
        if 'thumbnail' in request.data:
            post.thumbnail = request.data['thumbnail']
        post.save()
        serializer = PostSerializer(post)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
