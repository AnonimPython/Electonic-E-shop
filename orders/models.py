from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Общая сумма'
    )


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.id} от {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Товар'
    )
    product_name = models.CharField(max_length=255, verbose_name='Название товара на момент заказа')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'