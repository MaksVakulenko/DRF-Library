from django.urls import path, include
from rest_framework.routers import DefaultRouter

from payment.views import StripeSuccessAPI, StripeCancelAPI, PaymentViewSet


app_name = "payment"

router = DefaultRouter()
router.register('payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path("stripe/success/", StripeSuccessAPI.as_view(), name="stripe-success"),
    path("stripe/cancel/", StripeCancelAPI.as_view(), name="stripe-cancel"),
]
