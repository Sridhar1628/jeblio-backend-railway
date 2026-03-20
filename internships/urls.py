from django.urls import path
from .views import (InternshipApplicationView, UpdateApplicationStatusView, InternshipApplicationListView,
                    DeleteApplicationView, get_application_count)


urlpatterns = [
    path('apply/', InternshipApplicationView.as_view()),
    path('update-status/<int:pk>/', UpdateApplicationStatusView.as_view()),
    path('all/', InternshipApplicationListView.as_view()),
    path('delete/<int:pk>/', DeleteApplicationView.as_view()),
    path('application-count/', get_application_count),
]