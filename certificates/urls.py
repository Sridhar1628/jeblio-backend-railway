from django.urls import path
from .views import UploadExcelView, DownloadReportView, CertificateVerifyView

urlpatterns = [
    path('upload/', UploadExcelView.as_view()),
    path('download/', DownloadReportView.as_view()),
    path('verify/<str:cert_id>/', CertificateVerifyView.as_view(), name='verify-certificate')
]