import datetime
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from .models import Profile, CartItem, Order, City, District, Section, Building
from .serializers import UserSerializer, ProfileSerializer, CartItemSerializer, OrderSerializer, CitySerializer, DistrictSerializer, SectionSerializer, BuildingSerializer
from rest_framework import viewsets
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.adapter import get_adapter
from items.models import Item
from rest_framework.authtoken.models import Token


class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all().order_by('name')


class DistrictViewSet(viewsets.ModelViewSet):
    serializer_class = DistrictSerializer
    queryset = District.objects.all().order_by('name')

    def get_queryset(self):
        queryset = District.objects.all().order_by('name')
        city = self.request.query_params.get('city', None)
        if city is not None:
            queryset = queryset.filter(city=int(city)).distinct()
        return queryset

    def create(self, request, *args, **kwargs):
        if 'city' in request.data and 'name' in request.data:
            city_id = int(request.data['city'])
            city = City.objects.get(id=city_id)
            district = District.objects.create(
                city=city, name=request.data['name'])
            serializer = DistrictSerializer(district)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def update(self, request, *args, **kwargs):
        district = self.get_object()
        if 'city' in request.data:
            city_id = int(request.data['city'])
            city = City.objects.get(id=city_id)
            district.city = city
        if 'name' in request.data:
            district.name = request.data['name']
        serializer = DistrictSerializer(district)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer
    queryset = Section.objects.all().order_by('name')

    def get_queryset(self):
        queryset = Section.objects.all().order_by('name')
        district = self.request.query_params.get('district', None)
        if district is not None:
            queryset = queryset.filter(district=int(district)).distinct()
        return queryset

    def create(self, request, *args, **kwargs):
        if 'district' in request.data and 'name' in request.data:
            district_id = int(request.data['district'])
            district = District.objects.get(id=district_id)
            section = Section.objects.create(
                district=district, name=request.data['name'])
            serializer = SectionSerializer(section)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def update(self, request, *args, **kwargs):
        section = self.get_object()
        if 'district' in request.data:
            district_id = int(request.data['district'])
            district = District.objects.get(id=district_id)
            section.district = district
        if 'name' in request.data:
            section.name = request.data['name']
        serializer = SectionSerializer(section)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class BuildingViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingSerializer
    queryset = Building.objects.all().order_by('name')

    def get_queryset(self):
        queryset = Building.objects.all().order_by('name')
        section = self.request.query_params.get('section', None)
        if section is not None:
            queryset = queryset.filter(section=int(section)).distinct()
        return queryset

    def create(self, request, *args, **kwargs):
        if 'section' in request.data and 'name' in request.data:
            section_id = int(request.data['section'])
            section = Section.objects.get(id=section_id)
            building = Building.objects.create(
                section=section, name=request.data['name'])
            serializer = BuildingSerializer(building)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def update(self, request, *args, **kwargs):
        building = self.get_object()
        if 'section' in request.data:
            section_id = int(request.data['section'])
            section = Section.objects.get(id=section_id)
            building.section = section
        if 'name' in request.data:
            building.name = request.data['name']
        serializer = BuildingSerializer(building)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all().order_by('id')


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all().order_by('id')

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        user = profile.user
        if 'username' in request.data:
            user.username = request.data['username']
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        if 'phone_number' in request.data:
            profile.phone_number = request.data['phone_number']
        if 'birth_date' in request.data:
            profile.birth_date = request.data['birth_date']
        if 'address' in request.data:
            profile.address = request.data['address']
        if 'role' in request.data:
            profile.role = request.data['role']
        if 'favorite' in request.data:
            item = Item.objects.get(id=int(request.data['item']))
            if item in profile.favorite.all():
                profile.favorite.remove(item)
            else:
                profile.favorite.add(item)
        if 'cart' in request.data:
            item = Item.objects.get(id=int(request.data['item']))
            count = int(request.data['count'])
            mode = request.data['mode']
            if mode == "create":
                cartitem = CartItem.objects.create(
                    item=item,
                    count=count
                )
                profile.cart.add(cartitem)
            elif mode == "delete":
                profile.cart.all().filter(item=item).first().delete()
            elif mode == "add":
                cartitem = profile.cart.all().filter(item=item).first()
                cartitem.count = cartitem.count + 1
                cartitem.save()
            elif mode == "sub":
                cartitem = profile.cart.all().filter(item=item).first()
                cartitem.count = cartitem.count - 1
                cartitem.save()
        profile.save()
        user.save()
        serializer = ProfileSerializer(profile)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')

def getBonus(items, percent):
    bonus = 0
    for order_item in items:
        item = order_item.item
        count = order_item.count
        if (item.is_featured == True):
            bonus = bonus + (item.price / 100) * percent * 1.5 * count
        else: 
            bonus = bonus + (item.price / 100) * percent * count
        item.total = item.total - count
        item.save()
    
    return bonus

def updatePercent(user):
    if user.profile.total > 5000:
        user.profile.percent = 3
        user.profile.level = 1
    elif user.profile.total > 20000:
        user.profile.percent = 4
        user.profile.level = 2
    elif user.profile.total > 50000:
        user.profile.percent = 5
        user.profile.level = 3
    elif user.profile.total > 100000:
        user.profile.percent = 6
        user.profile.level = 4
    user.save()

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.order_by('-created_at')

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-created_at')
        user = self.request.query_params.get('user', None)
        state = self.request.query_params.get('state', None)
        if user is not None:
            queryset = queryset.filter(
                user__id=user).distinct().order_by('state', '-created_at')
        if state is not None:
            queryset = queryset.filter(
                state=state).distinct().order_by('created_at')
        return queryset

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        total = int(request.data['total'])
        bonus = int(request.data['bonus'])
        if (user.profile.bonus >= bonus):
            order = Order.objects.create(
                user=user,
                total=total,
                bonus=bonus,
                phone_number=request.data['phone_number'],
                address=request.data['address'],
                info=request.data['info'],
            )
            for item in user.profile.cart.all():
                order.items.add(item)
            order.save()
            user.profile.cart.clear()
            user.profile.bonus = user.profile.bonus - bonus
            user.save()
            serializer = OrderSerializer(order)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(data=None, status=status.HTTP_406_NOT_ACCEPTABLE)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        state = request.data['state']
        if state == "1":
            # Payed
            order.state = "2"
        elif state == "2":
            # On Delivery
            order.state = "3"
            ##order.on_delivery_at = datetime.datetime.now()
        elif state == "3":
            # Delivered
            order.state = "4"
            bonus = getBonus(order.items.all(), order.user.profile.percent)
            order.user.profile.bonus = order.user.profile.bonus + bonus
            order.user.profile.total = order.user.profile.total + bonus
            order.user.save()
            updatePercent(order.user)            
        elif state == "5":
            # Declined
            order.state = "5"
            order.user.profile.bonus = order.user.profile.bonus + order.bonus
            order.user.save()
        order.save()
        serializer = OrderSerializer(order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    callback_url = 'https://emhurgelt.mn/'
    client_class = OAuth2Client

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'https://emhurgelt.mn/'
    client_class = OAuth2Client

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)
