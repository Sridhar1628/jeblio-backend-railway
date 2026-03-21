from django.urls import path
from .views import (UploadExcelView, DownloadReportView, CertificateVerifyView, CertificateListView, DeleteCertificateView,
                    DeleteAllCertificatesView)

urlpatterns = [
    path('upload/', UploadExcelView.as_view()),
    path('download/', DownloadReportView.as_view()),
    path('verify/<str:cert_id>/', CertificateVerifyView.as_view(), name='verify-certificate'),
    # NEW 🔥
    path('history/', CertificateListView.as_view(), name='certificate-history'),
    path('delete/<str:cert_id>/', DeleteCertificateView.as_view(), name='delete-certificate'),
    path('delete-all/', DeleteAllCertificatesView.as_view(), name='delete-all-certificates'),
]