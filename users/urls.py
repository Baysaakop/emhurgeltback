from .views import UserViewSet, ProfileViewSet, OrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'profiles', ProfileViewSet, basename='profiles')
router.register(r'orders', OrderViewSet, basename='orders')
urlpatterns = router.urls
