from django.urls import path

from payment.views import StripeSuccessAPI, StripeCancelAPI


app_name = "payment"

urlpatterns = [
    path("stripe/success/", StripeSuccessAPI.as_view(), name="stripe-success"),
    path("stripe/cancel/", StripeCancelAPI.as_view(), name="stripe-cancel"),
]
