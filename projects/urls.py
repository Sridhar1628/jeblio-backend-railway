from django.urls import path
from .views import ProjectInquiryCreateView, UpdateProjectStatusView, ProjectInquiryListView

urlpatterns = [
    path('contact/', ProjectInquiryCreateView.as_view()),
    path('update-status/<int:pk>/', UpdateProjectStatusView.as_view()),
    path('list/', ProjectInquiryListView.as_view()),
]