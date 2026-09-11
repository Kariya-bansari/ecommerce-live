# ============================================================
# FILE: store/models.py
# ============================================================
from django.db import models
from django.contrib.auth.models import User


# ✅ No Product model here — products live in adminpanel_product table
# Cart, Wishlist, Order all reference product_id (bigint) directly


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.BigIntegerField()   # references adminpanel_product.id
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'store_cart'             # uses existing store_cart table
        unique_together = ('user', 'product_id')

    def __str__(self):
        return f"{self.user.username} → product #{self.product_id}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product_id = models.BigIntegerField(null=True)   # references adminpanel_product.id
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.CharField(max_length=500, blank=True)

    class Meta:
        db_table = 'store_wishlist'         # uses existing store_wishlist table
        unique_together = ('user', 'product_id')

    def __str__(self):
        return self.product_name


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('UPI', 'UPI'),
        ('CARD', 'Card'),
        ('NETBANKING', 'Net Banking'),
    ]
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('RETURNED', 'Returned'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='COD')
    total_amount = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'store_order'

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.BigIntegerField()   # references adminpanel_product.id
    quantity = models.IntegerField()
    price = models.FloatField()

    class Meta:
        db_table = 'store_orderitem'

    def __str__(self):
        return f"Product #{self.product_id} x{self.quantity}"