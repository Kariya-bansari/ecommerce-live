import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.db import connection

sql = 'ALTER TABLE store_orderitem DROP CONSTRAINT IF EXISTS store_orderitem_product_id_f2b098d4_fk_store_product_id;'
try:
    with connection.cursor() as cursor:
        cursor.execute(sql)
    print("Constraint dropped successfully!")
except Exception as e:
    print(f"Error dropping constraint: {e}")
