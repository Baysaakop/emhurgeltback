from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import CartItemSerializer, CustomUserSerializer
from .models import CartItem, CustomUser

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
            elif mode == "delete":
                customuser.cart.all().filter(item=item).first().delete()
            elif mode == "add":
                cartitem = customuser.cart.all().filter(item=item).first()
                cartitem.count = cartitem.count + 1
                cartitem.save()
            elif mode == "sub":
                cartitem = customuser.cart.all().filter(item=item).first()
                cartitem.count = cartitem.count - 1
                cartitem.save()
        customuser.save()
        serializer = CustomUserSerializer(customuser)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


# def getBonus(items, percent):
#     bonus = 0
#     for order_item in items:
#         item = order_item.item
#         count = order_item.count
#         if (item.is_featured == True):
#             bonus = bonus + (item.price / 100) * percent * 1.5 * count
#         else:
#             bonus = bonus + (item.price / 100) * percent * count
#         item.total = item.total - count
#         item.save()

#     return bonus


# def updatePercent(user):
#     if user.profile.total > 5000:
#         user.profile.percent = 3
#         user.profile.level = 1
#     elif user.profile.total > 20000:
#         user.profile.percent = 4
#         user.profile.level = 2
#     elif user.profile.total > 50000:
#         user.profile.percent = 5
#         user.profile.level = 3
#     elif user.profile.total > 100000:
#         user.profile.percent = 6
#         user.profile.level = 4
#     user.save()


# class OrderViewSet(viewsets.ModelViewSet):
#     serializer_class = OrderSerializer
#     queryset = Order.objects.order_by('-created_at')

#     def get_queryset(self):
#         queryset = Order.objects.all().order_by('-created_at')
#         user = self.request.query_params.get('user', None)
#         state = self.request.query_params.get('state', None)
#         if user is not None:
#             queryset = queryset.filter(
#                 user__id=user).distinct().order_by('state', '-created_at')
#         if state is not None:
#             queryset = queryset.filter(
#                 state=state).distinct().order_by('created_at')
#         return queryset

#     def create(self, request, *args, **kwargs):
#         user = Token.objects.get(key=request.data['token']).user
#         total = int(request.data['total'])
#         bonus = int(request.data['bonus'])
#         if (user.profile.bonus >= bonus):
#             order = Order.objects.create(
#                 user=user,
#                 total=total,
#                 bonus=bonus,
#                 phone_number=request.data['phone_number'],
#                 address=request.data['address'],
#                 info=request.data['info'],
#             )
#             for item in user.profile.cart.all():
#                 order.items.add(item)
#             order.save()
#             user.profile.cart.clear()
#             user.profile.bonus = user.profile.bonus - bonus
#             user.save()
#             serializer = OrderSerializer(order)
#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#         else:
#             return Response(data=None, status=status.HTTP_406_NOT_ACCEPTABLE)

#     def update(self, request, *args, **kwargs):
#         order = self.get_object()
#         state = request.data['state']
#         if state == "1":
#             # Payed
#             order.state = "2"
#         elif state == "2":
#             # On Delivery
#             order.state = "3"
#             ##order.on_delivery_at = datetime.datetime.now()
#         elif state == "3":
#             # Delivered
#             order.state = "4"
#             bonus = getBonus(order.items.all(), order.user.profile.percent)
#             order.user.profile.bonus = order.user.profile.bonus + bonus
#             order.user.profile.total = order.user.profile.total + bonus
#             order.user.save()
#             updatePercent(order.user)
#         elif state == "5":
#             # Declined
#             order.state = "5"
#             order.user.profile.bonus = order.user.profile.bonus + order.bonus
#             order.user.save()
#         order.save()
#         serializer = OrderSerializer(order)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
