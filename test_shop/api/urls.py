from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet,
    ProductViewSet,
    ShoppingCartViewSet,
    SubcategoryViewSet,
)


router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('subcategories', SubcategoryViewSet, basename='subcategories')
router.register('products', ProductViewSet, basename='products')
router.register('shoppingcart', ShoppingCartViewSet, basename='shoppingcart')

urlpatterns = [
    path('', include(router.urls)),
]
