import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

application = get_wsgi_application()

try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("ALTER TABLE store_orderitem DROP CONSTRAINT IF EXISTS store_orderitem_product_id_f2b098d4_fk_store_product_id;")
        cursor.execute("ALTER TABLE store_cart DROP CONSTRAINT IF EXISTS store_cart_product_id_41a1a5b8_fk_store_product_id;")
        cursor.execute("ALTER TABLE store_wishlist DROP CONSTRAINT IF EXISTS store_wishlist_product_id_f95cd32d_fk_store_product_id;")
except Exception as e:
    print("Could not drop constraint:", e)
