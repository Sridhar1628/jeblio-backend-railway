from rest_framework import generics

from unlock_engine.models.pass_models import Pass

from unlock_engine.api.serializers.pass_serializers import (
    PassSerializer,
    CreatePassSerializer,
    UpdatePassSerializer
)


class PassListCreateAPIView(
    generics.ListCreateAPIView
):
    queryset = Pass.objects.all().order_by('-created_at')

    def get_serializer_class(self):

        if self.request.method == 'POST':
            return CreatePassSerializer

        return PassSerializer


class PassRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Pass.objects.all()

    def get_serializer_class(self):

        if self.request.method in ['PUT', 'PATCH']:
            return UpdatePassSerializer

        return PassSerializer