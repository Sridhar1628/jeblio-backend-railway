from django.urls import path

from unlock_engine.api.views.lead_views import (
    LeadListCreateAPIView,
    LeadRetrieveUpdateDestroyAPIView,
    ClaimRewardAPIView
)

urlpatterns = [

    path(
        '',
        LeadListCreateAPIView.as_view(),
        name='lead-list-create'
    ),

    path(
        '<int:pk>/',
        LeadRetrieveUpdateDestroyAPIView.as_view(),
        name='lead-detail'
    ),
    path(
        '<int:pk>/claim-reward/',
        ClaimRewardAPIView.as_view(),
        name='claim-reward'
    ),
]