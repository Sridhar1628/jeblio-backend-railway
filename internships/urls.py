from django.urls import path
from .views import InternshipApplicationView, UpdateApplicationStatusView, InternshipApplicationListView

urlpatterns = [
    path('apply/', InternshipApplicationView.as_view()),
    path('update-status/<int:pk>/', UpdateApplicationStatusView.as_view()),
    path('all/', InternshipApplicationListView.as_view()),
]