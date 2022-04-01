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
        level = self.request.query_params.get('level', None)
        role = self.request.query_params.get('role', None)
        sortby = self.request.query_params.get('sortby', None)
        bonus_collected = self.request.query_params.get(
            'bonus_collected', None)
        if is_confirmed is not None:
            if is_confirmed == "True":
                queryset = queryset.filter(is_confirmed=True).distinct()
            else:
                queryset = queryset.filter(is_confirmed=False).distinct()
        if role is not None:
            queryset = queryset.filter(role=int(role)).distinct()
        if level is not None:
            queryset = queryset.filter(level=int(level)).distinct()
        if bonus_collected is not None:
            if bonus_collected == "True":
                queryset = queryset.filter(bonus_collected=True).distinct()
            else:
                queryset = queryset.filter(bonus_collected=False).distinct()
        if sortby is not None:
            queryset = queryset.order_by(sortby)
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
        if 'bonus_collected' in request.data:
            type = request.data['type']
            if customuser.bonus_collected == False:
                customuser.bonus_collected = True
                if type == "bonus":
                    customuser.bonus += 2500000
            else:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
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
    page_size = 36


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.order_by('-created_at')
    pagination_class = OrderPagination

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-created_at')
        customer = self.request.query_params.get('customer', None)
        is_payed = self.request.query_params.get('is_payed', None)
        datemin = self.request.query_params.get('datemin', None)
        datemax = self.request.query_params.get('datemax', None)
        sortby = self.request.query_params.get('sortby', None)
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
        if datemin is not None and datemax is not None:
            queryset = queryset.filter(
                created_at__range=[datemin, datemax]).distinct().order_by('-created_at')
        if sortby is not None:
            queryset = queryset.order_by(sortby)
        return queryset

    def create(self, request, *args, **kwargs):
        customer = Token.objects.get(key=request.data['token']).user
        total = int(request.data['total'])
        bonus_used = int(request.data['bonus_used'])
        if (customer.bonus >= bonus_used):
            order = Order.objects.create(
                customer=customer,
                total=total,
                bonus_used=bonus_used,
                phone_number=request.data['phone_number'],
                address=request.data['address']
            )
            for cartitem in customer.cart.all():
                order.items.add(cartitem)
                cartitem.item.count -= cartitem.count
                cartitem.item.save()
            order.save()
            customer.cart.clear()
            customer.bonus -= bonus_used
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
            order.bonus_granted = bonus
            order.customer.bonus += bonus
            order.customer.total += order.total - order.bonus_used
            level = getLevel(order.customer.total)
            if order.customer.level != level:
                order.customer.level = level
                if level == 2:
                    order.customer.bonus += 300000
            order.customer.save()
        if 'is_delivered' in request.data and request.data['is_delivered'] == True:
            order.is_delivered = True
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
