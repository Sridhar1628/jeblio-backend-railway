from django.urls import path
from .views import UploadExcelView, DownloadReportView

urlpatterns = [
    path('upload/', UploadExcelView.as_view()),
    path('download/', DownloadReportView.as_view()),
]