from django.db import models


# ================= REGISTER MODEL (Legacy - kept for DB compatibility) =================
# NOTE: Authentication is now handled by Django's built-in User model (auth_user table).
# This model is retained only if you need to reference old tbl_register data.
class Register(models.Model):
    id       = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email    = models.EmailField()
    password = models.CharField(max_length=100)

    class Meta:
        db_table = "tbl_register"

    def __str__(self):
        return self.username


# ================= PRODUCT MODEL =================
class Product(models.Model):
    product_id   = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    category     = models.CharField(max_length=50)
    brand        = models.CharField(max_length=50)
    model_type   = models.CharField(max_length=50)
    quantity     = models.IntegerField()
    unit_price   = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percent  = models.DecimalField(max_digits=5, decimal_places=2)
    total_price  = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.CharField(max_length=255)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.product_name


# ================= ORDER MODEL =================
class Order(models.Model):
    order_id         = models.AutoField(primary_key=True)
    full_name        = models.CharField(max_length=150)
    email            = models.EmailField()
    product_name     = models.CharField(max_length=150)
    quantity         = models.IntegerField()
    payment_method   = models.CharField(max_length=50)
    shipping_address = models.TextField()
    order_date       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders"

    def __str__(self):
        return f"Order #{self.order_id} - {self.full_name}"