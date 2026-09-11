# ============================================================
# FILE: ecommerce20-2-26/ecommerce20-2-26/urls.py  (main project urls.py)
# ============================================================
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from accounts.views import login_view, register, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),

    # Login, Register & Logout
    path("login/", login_view, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout_view, name="logout"),

    # ✅ FIXED: Store App now at /product/ (matches all your templates)
    path("product/", include("store.urls")),

    # Other apps
    path("accounts/", include("accounts.urls")),
    path("feedback/", include("feedbackapp.urls")),
    path("contact/", include("contact.urls")),
    path("gallery/", include("galleryapp.urls")),

    # ❌ REMOVED: path('wishlist/', include('wishlist.urls'))
    #    — there is no separate wishlist app in your DB.
    #      Wishlist is handled inside store app at /product/wishlist/

    # Admin Panel (homepage etc.)
    path("", include("adminpanel.urls")),

    # Static template pages
    path("about1/", TemplateView.as_view(template_name="about1.html"), name="about1"),
    path("profile/", TemplateView.as_view(template_name="profile.html"), name="profile"),
    path("same-day-delivery/", TemplateView.as_view(template_name="same_day_delivery.html"), name="same_day_delivery"),
    path("installation-repair/", TemplateView.as_view(template_name="installation-repair.html"), name="installation-repair"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    from django.views.static import serve
    from django.urls import re_path
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]