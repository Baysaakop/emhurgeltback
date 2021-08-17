from .views import UserViewSet, ProfileViewSet, OrderViewSet, CityViewSet, DistrictViewSet, SectionViewSet, BuildingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'profiles', ProfileViewSet, basename='profiles')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'cities', CityViewSet, basename='cities')
router.register(r'districts', DistrictViewSet, basename='districts')
router.register(r'sections', SectionViewSet, basename='sections')
router.register(r'buildings', BuildingViewSet, basename='buildings')
urlpatterns = router.urls
