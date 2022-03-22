from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet, CustomUserViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'orders', OrderViewSet, basename='orders')
urlpatterns = router.urls
