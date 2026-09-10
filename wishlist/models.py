from django.db import models

class Wishlist(models.Model):
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='wishlist/')

    def __str__(self):
        return self.product_name