from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from library_service.views import health_check


urlpatterns = [
    # Django Admin Panel
    path("admin/", admin.site.urls),
    # Healthcheck endpoint
    path("api/health/", health_check, name="health_check"),
    # Spectacular:
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/library/", include("book.urls", namespace="book")),
    path("api/library/", include("borrowing.urls", namespace="borrowing")),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/payment/", include("payment.urls", namespace="payment")),
] + debug_toolbar_urls()
