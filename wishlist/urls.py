from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist_page, name='wishlist'),
    path('add/', views.add_wishlist, name='add_wishlist'),
]