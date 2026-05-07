from django.urls import path
from .views import  create_order, verify_payment, CreateInitialSuperAdminView

urlpatterns = [
    path('create-order/', create_order),
    path('verify-payment/', verify_payment),
     path(
        "setup/create-super-admin/",
        CreateInitialSuperAdminView.as_view(),
        name="create-super-admin",
    ),
]