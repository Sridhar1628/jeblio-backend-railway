from rest_framework import generics

from unlock_engine.models.reward_models import Reward

from unlock_engine.api.serializers.reward_serializers import (
    RewardSerializer,
    CreateRewardSerializer,
    UpdateRewardSerializer
)


class RewardListCreateAPIView(
    generics.ListCreateAPIView
):
    queryset = Reward.objects.all().order_by('-created_at')

    def get_serializer_class(self):

        if self.request.method == 'POST':
            return CreateRewardSerializer

        return RewardSerializer


class RewardRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Reward.objects.all()

    def get_serializer_class(self):

        if self.request.method in ['PUT', 'PATCH']:
            return UpdateRewardSerializer

        return RewardSerializer