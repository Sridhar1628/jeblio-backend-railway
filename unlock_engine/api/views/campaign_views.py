from rest_framework import generics

from unlock_engine.models.campaign_models import Campaign

from unlock_engine.api.serializers.campaign_serializers import (
    CampaignSerializer,
    CreateCampaignSerializer,
    UpdateCampaignSerializer
)


class CampaignListCreateAPIView(
    generics.ListCreateAPIView
):
    queryset = Campaign.objects.all().order_by('-created_at')

    def get_serializer_class(self):

        if self.request.method == 'POST':
            return CreateCampaignSerializer

        return CampaignSerializer


class CampaignRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Campaign.objects.all()

    def get_serializer_class(self):

        if self.request.method in ['PUT', 'PATCH']:
            return UpdateCampaignSerializer

        return CampaignSerializer