from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Spectacular:
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path("api/library/", include("book.urls", namespace="book")),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/payment/", include("payment.urls", namespace="payment")),
] + debug_toolbar_urls()
