from django.urls import path

from unlock_engine.api.views.campaign_views import (
    CampaignListCreateAPIView,
    CampaignRetrieveUpdateDestroyAPIView
)

urlpatterns = [

    path(
        '',
        CampaignListCreateAPIView.as_view(),
        name='campaign-list-create'
    ),

    path(
        '<int:pk>/',
        CampaignRetrieveUpdateDestroyAPIView.as_view(),
        name='campaign-detail'
    ),
]