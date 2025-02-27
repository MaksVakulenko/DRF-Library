from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/payment/", include("payment.urls", namespace="payment")),
    path("api/user/", include("user.urls", namespace="user")),
] + debug_toolbar_urls()
