# ============================================================
# FILE: adminpanel/models.py
# ============================================================
from django.db import models


class Product(models.Model):
    Product_Name = models.CharField(max_length=255)
    Brand = models.CharField(max_length=100)
    Category = models.CharField(max_length=100)
    Model_Type = models.CharField(max_length=100)
    Quantity = models.IntegerField()
    Unit_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Gst_Percent = models.DecimalField(max_digits=5, decimal_places=2)
    Total_Price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ProductImage = models.ImageField(upload_to='products/', blank=True, null=True)

    class Meta:
        db_table = 'adminpanel_product'   # maps exactly to your existing table

    def __str__(self):
        return self.Product_Name

    # Helper: use Quantity as Stock for product_list.html compatibility
    @property
    def Stock(self):
        return self.Quantity