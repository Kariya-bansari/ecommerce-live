from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),  # opens /gallery/
    path('admin-add/', views.admin_add_gallery, name='admin_add_gallery'),
]