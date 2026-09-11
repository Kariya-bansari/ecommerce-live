# ============================================================
# FILE: store/urls.py
# ============================================================
from django.urls import path
from . import views

urlpatterns = [
    # Product list page — http://127.0.0.1:8000/product/
    path('', views.product_list, name='product_list'),

    # Cart pages
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/toggle-ajax/<int:id>/', views.toggle_cart_ajax, name='toggle_cart_ajax'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_cart, name='remove_cart'),

    # Wishlist pages — http://127.0.0.1:8000/product/wishlist/
    path('wishlist/', views.wishlist_view, name='store_wishlist'),
    path('wishlist/toggle-ajax/<int:id>/', views.toggle_wishlist_ajax, name='toggle_wishlist_ajax'),

    # Order pages
    path('order/<int:id>/', views.order_form, name='order_form'),
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<int:order_id>/track/', views.track_order, name='track_order'),
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('orders/<int:order_id>/return/', views.return_order, name='return_order'),
]