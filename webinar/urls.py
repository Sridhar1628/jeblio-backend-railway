from django.urls import path
from .views import get_terms, create_order, verify_payment

urlpatterns = [
    path('terms/', get_terms),
    path('create-order/', create_order),
    path('verify-payment/', verify_payment),
]