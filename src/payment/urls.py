from django.urls import path, include
from rest_framework.routers import DefaultRouter

from payment.views import StripeSuccessAPI, StripeCancelAPI, PaymentViewSet, CancelPaymentAPIView

app_name = "payment"

router = DefaultRouter()
router.register('payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path("stripe/success/", StripeSuccessAPI.as_view(), name="stripe-success"),
    path("stripe/cancel/", StripeCancelAPI.as_view(), name="stripe-cancel"),
    path("cancel/<int:pk>/", CancelPaymentAPIView.as_view(), name="payment-cancel"),

]
