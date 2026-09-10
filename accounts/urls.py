from django.urls import path
from . import views

urlpatterns = [
    path("",          views.home,           name="home"),
    path("register/", views.register,        name="register"),
    path("login/",    views.login_view,      name="login"),
    path("logout/",   views.logout_view,     name="logout"),
    path("dashboard/",views.dashboard,       name="dashboard"),

    # Product API
    path("api/add-product/", views.api_add_product, name="api_add_product"),
    path("api/products/",    views.api_products,    name="api_products"),

    # Order
    path("place-order/",     views.place_order,     name="accounts_place_order"),
]