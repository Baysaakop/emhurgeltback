from .views import UserViewSet, ProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')
router.register(r'profiles', ProfileViewSet, basename='profiles')
urlpatterns = router.urls