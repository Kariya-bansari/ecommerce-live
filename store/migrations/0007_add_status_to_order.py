from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_alter_order_payment_mode_alter_product_stock_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("CONFIRMED", "Confirmed"),
                    ("PROCESSING", "Processing"),
                    ("SHIPPED", "Shipped"),
                    ("OUT_FOR_DELIVERY", "Out for Delivery"),
                    ("DELIVERED", "Delivered"),
                    ("CANCELLED", "Cancelled"),
                    ("RETURNED", "Returned"),
                ],
                default="CONFIRMED",
                max_length=20,
            ),
        ),
    ]
