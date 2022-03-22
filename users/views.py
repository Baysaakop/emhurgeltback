from rest_framework import viewsets, status, pagination
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import CartItemSerializer, CustomUserSerializer, OrderSerializer
from .models import CartItem, CustomUser, Order

from items.models import Item


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all().order_by('id')


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all().order_by('id')

    def get_queryset(self):
        queryset = CustomUser.objects.all().order_by('id')
        is_confirmed = self.request.query_params.get('is_confirmed', None)
        role = self.request.query_params.get('role', None)
        if is_confirmed is not None:
            if is_confirmed == "True":
                queryset = queryset.filter(is_confirmed=True).distinct()
            else:
                queryset = queryset.filter(is_confirmed=False).distinct()
        if role is not None:
            queryset = queryset.filter(role=int(role)).distinct()
        return queryset

    def update(self, request, *args, **kwargs):
        customuser = self.get_object()
        if 'username' in request.data:
            customuser.username = request.data['username']
        if 'email' in request.data:
            customuser.email = request.data['email']
        if 'company_name' in request.data:
            customuser.company_name = request.data['company_name']
        if 'company_id' in request.data:
            customuser.company_id = request.data['company_id']
        if 'address' in request.data:
            customuser.address = request.data['address']
        if 'is_confirmed' in request.data:
            customuser.is_confirmed = True
        if 'role' in request.data:
            customuser.role = request.data['role']
        if 'favorite' in request.data:
            item = Item.objects.get(id=int(request.data['item']))
            if item in customuser.favorite.all():
                customuser.favorite.remove(item)
            else:
                customuser.favorite.add(item)
        if 'cart' in request.data:
            item = Item.objects.get(id=int(request.data['item']))
            count = int(request.data['count'])
            mode = request.data['mode']
            if mode == "create":
                cartitem = CartItem.objects.create(
                    item=item,
                    count=count
                )
                customuser.cart.add(cartitem)
            elif mode == "update":
                cartitem = customuser.cart.all().filter(item=item).first()
                cartitem.count = count
                cartitem.save()
            elif mode == "delete":
                customuser.cart.all().filter(item=item).first().delete()
        customuser.save()
        serializer = CustomUserSerializer(customuser)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


def getLevel(total):
    if total >= 88000000:
        return 3
    elif total >= 33000000:
        return 2
    else:
        return 1


class OrderPagination(pagination.PageNumberPagination):
    page_size = 24


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.order_by('-created_at')
    pagination_class = OrderPagination

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-created_at')
        customer = self.request.query_params.get('customer', None)
        is_payed = self.request.query_params.get('is_payed', None)
        if customer is not None:
            queryset = queryset.filter(
                customer__id=customer).distinct().order_by('-created_at')
        if is_payed is not None:
            if is_payed == "True":
                queryset = queryset.filter(
                    is_payed=True).distinct().order_by('-created_at')
            else:
                queryset = queryset.filter(
                    is_payed=False).distinct().order_by('-created_at')
        return queryset

    def create(self, request, *args, **kwargs):
        customer = Token.objects.get(key=request.data['token']).user
        total = int(request.data['total'])
        bonus = int(request.data['bonus'])
        if (customer.bonus >= bonus):
            order = Order.objects.create(
                customer=customer,
                total=total,
                bonus=bonus,
                phone_number=request.data['phone_number'],
                address=request.data['address']
            )
            for cartitem in customer.cart.all():
                order.items.add(cartitem)
                cartitem.item.count -= cartitem.count
                cartitem.item.save()
            order.save()
            customer.cart.clear()
            customer.bonus -= bonus
            customer.save()
            serializer = OrderSerializer(order)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(data=None, status=status.HTTP_406_NOT_ACCEPTABLE)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if 'is_payed' in request.data and request.data['is_payed'] == True:
            order.is_payed = True
            bonus = 0
            for cartitem in order.items.all():
                bonus += (cartitem.item.price / 100) * cartitem.item.multiplier * \
                    order.customer.level * cartitem.count
            order.customer.bonus += bonus
            order.customer.total += order.total
            order.customer.level = getLevel(order.customer.total)
            order.customer.save()
        order.save()
        serializer = OrderSerializer(order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        for cartitem in order.items.all():
            cartitem.item.count += cartitem.count
            cartitem.item.save()
        order.customer.bonus += order.bonus
        order.customer.save()
        return super().destroy(request, *args, **kwargs)
