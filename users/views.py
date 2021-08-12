import datetime
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from .models import Profile, CartItem, Order
from .serializers import UserSerializer, ProfileSerializer, CartItemSerializer, OrderSerializer
from rest_framework import viewsets
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.adapter import get_adapter
from addresses.models import Address, City, District
from items.models import Item
from rest_framework.authtoken.models import Token


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

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
            address, created = Address.objects.get_or_create(
                city=City.objects.get(id=int(request.data['city'])),
                district=District.objects.get(
                    id=int(request.data['district'])),
                section=request.data['section'],
                address=request.data['address']
            )
            profile.address = address
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
    queryset = User.objects.all()


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
            order.user.profile.bonus = order.user.profile.bonus + \
                ((order.total - order.bonus) / 100 * order.user.profile.point)
            order.user.save()
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
