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
        # Also add status column if not exists (safe migration fallback)
        cursor.execute("ALTER TABLE store_order ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'CONFIRMED';")
except Exception as e:
    print("Could not drop constraint:", e)

# Auto-create admin superuser on first deploy if not exists
try:
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@dharaenterprise.com',
            password='Dhara@2024'
        )
        print("Superuser created: admin / Dhara@2024")
except Exception as e:
    print("Superuser creation skipped:", e)
