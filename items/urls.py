from .views import CompanyViewSet, TypeViewSet, CategoryViewSet, SubCategoryViewSet, TagViewSet, ItemViewSet, SliderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='companies')
router.register(r'types', TypeViewSet, basename='types')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategories')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'items', ItemViewSet, basename='items')
router.register(r'sliders', SliderViewSet, basename='sliders')
urlpatterns = router.urls
