from rest_framework import serializers

from shop.models import Category, Product, ShoppingCart, SubCategory


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для отображения категорий."""

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'slug',
            'desc',
            'image',
        )


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для отображения подкатегорий."""

    category = CategorySerializer()

    class Meta:
        model = SubCategory
        fields = (
            'id',
            'name',
            'slug',
            'desc',
            'category',
            'image',
        )


class ShortenedSubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для укороченного отображения подкатегорий."""

    parent_category = serializers.CharField(source='category.name')

    class Meta:
        model = SubCategory
        fields = (
            'id',
            'name',
            'slug',
            'parent_category',
        )


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения товаров."""

    subcategory = ShortenedSubcategorySerializer()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'desc',
            'price',
            'subcategory',
            'image',
            'image_medium',
            'image_small',
        )


class ShortenedProductSerializer(serializers.ModelSerializer):
    """Сериализатор для укороченного отображения товаров."""

    subcategory = SubcategorySerializer()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'subcategory',
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения корзины."""

    product_name = serializers.CharField(source='product.name')
    product_price = serializers.IntegerField(source='product.price')

    class Meta:
        model = ShoppingCart
        fields = (
            'product_name',
            'product_price',
            'amount',
        )


class ShortenedShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для укороченного отображения корзины."""

    class Meta:
        model = ShoppingCart
        fields = (
            'product',
            'amount',
        )


class ShoppingCartWriteSerializer(serializers.ModelSerializer):
    """Сериализатор добавления в корзину объектов."""

    products = ShortenedShoppingCartSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'products',
        )

    def create(self, validated_data):
        shop_items: list[ShoppingCart] = []
        for item in validated_data['products']:
            shop_items.append(
                ShoppingCart(
                    user=validated_data['user'],
                    product=item['product'],
                    amount=item['amount'],
                )
            )
        objects: list[ShoppingCart] = (
            ShoppingCart.objects.bulk_create(shop_items)
        )
        self.context['objects'] = objects
        return objects

    def to_representation(self, instance):
        objects: list[ShoppingCart] = self.context['objects']
        count_products: int = len(objects)
        total: float = sum(
            object.good.price * object.amount for object in objects
        )
        products: list[dict[str, any]] = []
        for object in objects:
            products.append(
                {
                    'product': object.good.name,
                    'price': object.good.price,
                    'amount': object.amount,
                }
            )
        data = {
            'count_products': count_products,
            'totalsum': total,
            'products': products,
        }
        return data


class TotalShoppingCartSerializer(serializers.Serializer):
    """Сериализатор для отображения суммарных значений корзины."""

    count_products = serializers.IntegerField()
    totalsum = serializers.FloatField()
    products = ShoppingCartSerializer()

    class Meta:
        fields = (
            'count_products',
            'totalsum',
            'products',
        )
