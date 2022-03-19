from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Company, Type, Category, SubCategory, Tag, Item
from .serializers import CompanySerializer, TypeSerializer, CategorySerializer, SubCategorySerializer, TagSerializer, ItemSerializer


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


class TypeViewSet(viewsets.ModelViewSet):
    serializer_class = TypeSerializer
    queryset = Type.objects.all().order_by('id')


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('id')

    def get_queryset(self):
        queryset = Category.objects.all().order_by('id')
        type = self.request.query_params.get('type', None)
        types = self.request.query_params.get('types', None)
        if type is not None:
            queryset = queryset.filter(
                type=Type.objects.get(id=int(type))).distinct()
        if types is not None:
            arr = []
            for t in types.split(","):
                arr.append(int(t))
            queryset = queryset.filter(type__in=arr).distinct()
        return queryset

    def create(self, request, *args, **kwargs):
        type = Type.objects.get(id=int(request.data['type']))
        category = Category.objects.create(
            type=type,
            name=request.data['name']
        )
        if 'name_en' in request.data:
            category.name_en = request.data['name_en']
        if 'description' in request.data:
            category.description = request.data['description']
        category.save()
        serializer = CategorySerializer(category)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        if 'type' in request.data:
            type = Type.objects.get(id=int(request.data['type']))
            category.type = type
        if 'name' in request.data:
            category.name = request.data['name']
        if 'name_en' in request.data:
            category.name_en = request.data['name_en']
        if 'description' in request.data:
            category.description = request.data['description']
        category.save()
        serializer = CategorySerializer(category)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all().order_by('id')

    def get_queryset(self):
        queryset = SubCategory.objects.all().order_by('id')
        category = self.request.query_params.get('category', None)
        categories = self.request.query_params.get('categories', None)
        if category is not None:
            queryset = queryset.filter(
                category=Category.objects.get(id=int(category))).distinct()
        if categories is not None:
            arr = []
            for c in categories.split(","):
                arr.append(int(c))
            queryset = queryset.filter(category__in=arr).distinct()
        return queryset

    def create(self, request, *args, **kwargs):
        category = Category.objects.get(id=int(request.data['category']))
        subcategory = SubCategory.objects.create(
            category=category,
            name=request.data['name']
        )
        if 'name_en' in request.data:
            subcategory.name_en = request.data['name_en']
        if 'description' in request.data:
            subcategory.description = request.data['description']
        subcategory.save()
        serializer = SubCategorySerializer(subcategory)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        subcategory = self.get_object()
        if 'category' in request.data:
            category = Category.objects.get(id=int(request.data['category']))
            subcategory.category = category
        if 'name' in request.data:
            subcategory.name = request.data['name']
        if 'name_en' in request.data:
            subcategory.name_en = request.data['name_en']
        if 'description' in request.data:
            subcategory.description = request.data['description']
        subcategory.save()
        serializer = SubCategorySerializer(subcategory)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all().order_by('id')


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all().order_by('-is_featured', '-created_at')

    def get_queryset(self):
        queryset = Item.objects.all().order_by('-is_featured', '-created_at')
        name = self.request.query_params.get('name', None)
        is_featured = self.request.query_params.get('is_featured', None)
        type = self.request.query_params.get('type', None)
        category = self.request.query_params.get('category', None)
        subcategory = self.request.query_params.get('subcategory', None)
        tags = self.request.query_params.get('tags', None)
        pricelow = self.request.query_params.get('pricelow', None)
        pricehigh = self.request.query_params.get('pricehigh', None)
        order = self.request.query_params.get('order', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name).distinct()
            # queryset = queryset.filter(Q(name__icontains=name) | Q(tag__name=name)).distinct()
        if is_featured is not None:
            queryset = queryset.filter(is_featured=True).distinct()
        if type is not None:
            queryset = queryset.filter(types__id=type).distinct()
        if category is not None:
            queryset = queryset.filter(categories__id=category).distinct()
        if subcategory is not None:
            queryset = queryset.filter(
                subcategories__id=subcategory).distinct()
        # if tags is not None:
        #     for tag in tags.split(","):
        #         queryset = queryset.filter(tag__id=tag).distinct()
        if pricelow is not None:
            queryset = queryset.filter(price__gte=pricelow).distinct()
        if pricehigh is not None:
            queryset = queryset.filter(price__lt=pricehigh).distinct()
        if order is not None:
            queryset = queryset.order_by(order)
        return queryset

    def create(self, request, *args, **kwargs):
        item = Item.objects.create(
            name=request.data['name']
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
            item.price = int(request.data['price'])
        if 'count' in request.data:
            item.count = int(request.data['count'])
        if 'is_featured' in request.data:
            if request.data['is_featured'] == 'true':
                item.is_featured = True
            else:
                item.is_featured = False
        if 'company' in request.data:
            item.company = Company.objects.filter(
                id=int(request.data['company']))[0]
        if 'type' in request.data:
            types = request.data['type'].split(',')
            for t in types:
                item.types.add(
                    Type.objects.filter(id=int(t))[0])
        if 'category' in request.data:
            categories = request.data['category'].split(',')
            for c in categories:
                item.categories.add(
                    Category.objects.filter(id=int(c))[0])
        if 'subcategory' in request.data:
            subcategories = request.data['subcategory'].split(',')
            for s in subcategories:
                item.subcategories.add(
                    SubCategory.objects.filter(id=int(s))[0])
        # if 'tags' in request.data:
        #     tags = request.data['tags'].split(',')
        #     for tag in tags:
        #         item.tags.add(Tag.objects.filter(id=int(tag))[0])
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
        if 'video' in request.data:
            item.video = request.data['video']
        item.save()
        serializer = ItemSerializer(item)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        item = self.get_object()
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
            item.price = int(request.data['price'])
        if 'count' in request.data:
            item.count = int(request.data['count'])
        if 'is_featured' in request.data:
            if request.data['is_featured'] == 'true':
                item.is_featured = True
            else:
                item.is_featured = False
        if 'company' in request.data:
            item.company = Company.objects.filter(
                id=int(request.data['company']))[0]
        if 'type' in request.data:
            item.types.clear()
            types = request.data['type'].split(',')
            for t in types:
                item.types.add(
                    Type.objects.filter(id=int(t))[0])
        if 'category' in request.data:
            item.categories.clear()
            categories = request.data['category'].split(',')
            for c in categories:
                item.categories.add(
                    Category.objects.filter(id=int(c))[0])
        if 'subcategory' in request.data:
            item.subcategories.clear()
            subcategories = request.data['subcategory'].split(',')
            for s in subcategories:
                item.subcategories.add(
                    SubCategory.objects.filter(id=int(s))[0])
        # if 'tags' in request.data:
        #     tags = request.data['tags'].split(',')
        #     for tag in tags:
        #         item.tags.add(Tag.objects.filter(id=int(tag))[0])
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
        if 'video' in request.data:
            item.video = request.data['video']
        item.save()
        serializer = ItemSerializer(item)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
