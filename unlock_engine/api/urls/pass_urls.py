from django.urls import path

from unlock_engine.api.views.pass_views import (
    PassListCreateAPIView,
    PassRetrieveUpdateDestroyAPIView
)

urlpatterns = [

    path(
        '',
        PassListCreateAPIView.as_view(),
        name='pass-list-create'
    ),

    path(
        '<int:pk>/',
        PassRetrieveUpdateDestroyAPIView.as_view(),
        name='pass-detail'
    ),
]