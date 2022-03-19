from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet, CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
# router.register(r'profiles', ProfileViewSet, basename='profiles')
# router.register(r'orders', OrderViewSet, basename='orders')
urlpatterns = router.urls
