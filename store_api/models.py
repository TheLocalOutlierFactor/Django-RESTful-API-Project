from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01'))
        ]
    )
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name='products')

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0.01),
                name='price_gte_0.01',
            ),
        ]


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.product.price


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} on {self.product.name}'

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name='rating_range_1_to_5',
            ),
        ]


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'PND', _('Pending')
        PROCESSING = 'PRC', _('Processing')
        SHIPPED = 'SHP', _('Shipped')
        DELIVERED = 'DEL', _('Delivered')
        CANCELLED = 'CNL', _('Cancelled')
        RETURNED = 'RET', _('Returned')
        REFUNDED = 'REF', _('Refunded')
        FAILED = 'FLD', _('Failed')
        ON_HOLD = 'HLD', _('On Hold')
        PARTIALLY_SHIPPED = 'PSH', _('Partially Shipped')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=3,
        choices=OrderStatus,
        default=OrderStatus.PENDING,)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order {self.id} by {self.user.username} with status {self.status}'
