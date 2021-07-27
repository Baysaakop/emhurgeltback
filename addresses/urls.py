from .views import CityViewSet, DistrictViewSet, AddressViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='cities')
router.register(r'districts', DistrictViewSet, basename='districts')
router.register(r'addresses', AddressViewSet, basename='addresses')
urlpatterns = router.urls
