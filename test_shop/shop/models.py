from django.contrib.auth.models import User
from django.db import models

from test_shop.settings import set_image_name


class BaseModel(models.Model):
    """Модель темплейт."""
    slug = models.SlugField(max_length=64, unique=True)
    title = models.CharField(max_length=128, verbose_name='Название')
    desc = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(
        verbose_name='Основное изображение',
        upload_to=set_image_name,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Category(BaseModel):
    """Модель категорий."""
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class SubCategory(BaseModel):
    """Модель подкатегорий."""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategorys',
    )

    class Meta:
        verbose_name = 'подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(BaseModel):
    """Модель товаров."""
    price = models.PositiveIntegerField(
        verbose_name='Цена товара',
    )
    subcategory = models.ForeignKey(
        verbose_name='Подкатегория',
        to=SubCategory,
        related_name='product',
        on_delete=models.PROTECT,
    )
    image_medium = models.ImageField(
        verbose_name='Изображение (M)',
        upload_to=set_image_name,
    )
    image_small = models.ImageField(
        verbose_name='Изображение (S)',
        upload_to=set_image_name,
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ShoppingCart(models.Model):
    """
    Модель корзины товаров.
    """
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        related_name='shoppingcart_user',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        verbose_name='Товар',
        to=Product,
        related_name='shoppingcart_product',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'product'),
                name='unique_user_good',
            ),
        ]
        verbose_name = 'Корзина товаров'
        verbose_name_plural = 'Корзины товаров'

    def __str__(self):
        return f'{self.user}: {self.product.name} ({self.amount})'
