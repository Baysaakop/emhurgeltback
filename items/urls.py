from .views import CompanyViewSet, CategoryViewSet, SubCategoryViewSet, TagViewSet, ItemViewSet, SliderViewSet, VideoViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='companies')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategories')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'items', ItemViewSet, basename='items')
router.register(r'sliders', SliderViewSet, basename='sliders')
router.register(r'videos', VideoViewSet, basename='videos')
urlpatterns = router.urls
