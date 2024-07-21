from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import (
    CategorySerializer,
    SubcategorySerializer,
    ProductSerializer,
    ShoppingCartSerializer,
    ShoppingCartWriteSerializer,
)
from shop.models import Category, Product, ShoppingCart, SubCategory


class CategoryViewSet(ReadOnlyModelViewSet):
    """Вью для отображения категорий."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductViewSet(ReadOnlyModelViewSet):
    """Вью для отображения продуктов."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all().select_related('subcategory')


class ShoppingCartViewSet(ModelViewSet):
    """Вью для отображения корзины."""

    http_method_names = ('get', 'post',)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return ShoppingCart.objects.filter(
            user=self.request.user,
        ).select_related(
            'user',
            'product',
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShoppingCartSerializer
        return ShoppingCartWriteSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data: dict[str, any] = serializer.data
        count_products: int = len(data)
        total: float = sum(
            item.get('price', 0) * item.get('amount', 0) for item in data
        )
        return Response(
            data={
                'count_products': count_products,
                'totalsum': total,
                'productss': data
            },
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        data: dict[str, any] = request.data
        data['user'] = self.request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ShoppingCart.objects.filter(user=self.request.user).delete()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(
        methods=['post', ],
        detail=False,
        url_name='clear_shopping_cart',
    )
    def clear_shopping_cart(self, request):
        """Очищает корзину с товарами."""
        ShoppingCart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubcategoryViewSet(ReadOnlyModelViewSet):
    """Вью для отображения подкатегорий."""

    serializer_class = SubcategorySerializer
    queryset = SubCategory.objects.all().select_related('category')
