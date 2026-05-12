from django.urls import path

from unlock_engine.api.views.reward_views import (
    RewardListCreateAPIView,
    RewardRetrieveUpdateDestroyAPIView
)

urlpatterns = [

    path(
        '',
        RewardListCreateAPIView.as_view(),
        name='reward-list-create'
    ),

    path(
        '<int:pk>/',
        RewardRetrieveUpdateDestroyAPIView.as_view(),
        name='reward-detail'
    ),
]