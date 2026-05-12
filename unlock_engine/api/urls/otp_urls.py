from django.urls import path

from unlock_engine.api.views.otp_views import (
    VerifyOTPAPIView
)

urlpatterns = [

    path(
        'verify/',
        VerifyOTPAPIView.as_view(),
        name='verify-otp'
    ),
]