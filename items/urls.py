from .views import CompanyViewSet, CategoryViewSet, TagViewSet, ShopViewSet, ItemViewSet, PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='companies')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'shops', ShopViewSet, basename='shops')
router.register(r'items', ItemViewSet, basename='items')
router.register(r'posts', PostViewSet, basename='posts')
urlpatterns = router.urls
