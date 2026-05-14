from django.urls import path
from .views import  create_order, verify_payment, register_webinar

urlpatterns = [
    path('create-order/', create_order),
    path('verify-payment/', verify_payment),
    path(
    "register/",
    register_webinar,
    name="register_webinar"
),
]