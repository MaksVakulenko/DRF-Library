from django.urls import path, include

from payment.views import StripeSuccessAPI, StripeCancelAPI, PaymentListView, PaymentDetailView

app_name = "payment"

urlpatterns = [
    path("stripe/success/", StripeSuccessAPI.as_view(), name="stripe-success"),
    path("stripe/cancel/", StripeCancelAPI.as_view(), name="stripe-cancel"),
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path("payments/<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
]
