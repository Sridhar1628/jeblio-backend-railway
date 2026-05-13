from rest_framework import generics

from unlock_engine.models.pass_models import Pass

from unlock_engine.api.serializers.pass_serializers import (
    PassSerializer,
    CreatePassSerializer,
    UpdatePassSerializer
)
from rest_framework import status
from rest_framework.views import APIView, Response

from unlock_engine.api.serializers.pass_serializers import (
    BulkGeneratePassSerializer
)

from unlock_engine.services.bulk_pass_generation_service import (
    BulkPassGenerationService
)

from unlock_engine.api.serializers.pass_serializers import (
    ExportPassZipSerializer
)

from unlock_engine.services.pass_zip_export_service import (
    PassZipExportService
)

from unlock_engine.api.serializers.pass_serializers import (
    ExportPassPDFSerializer
)

from unlock_engine.services.pass_pdf_export_service import (
    PassPDFExportService
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
    
class PassByCodeAPIView(APIView):

    def get(self, request, pass_code):

        try:

            qr_pass = Pass.objects.get(
                pass_code=pass_code
            )

        except Pass.DoesNotExist:

            return Response(
                {
                    "error": "Pass not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PassSerializer(qr_pass)

        return Response(serializer.data)
    
class BulkGeneratePassAPIView(
    APIView
):

    def post(
        self,
        request
    ):

        serializer = (
            BulkGeneratePassSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        service = (
            BulkPassGenerationService()
        )

        result = service.generate_passes(
            serializer.validated_data
        )

        return Response(
            result,
            status=status.HTTP_201_CREATED
        )
    
class ExportPassZipAPIView(
    APIView
):

    def post(
        self,
        request
    ):

        serializer = (
            ExportPassZipSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        service = (
            PassZipExportService()
        )

        result = (
            service.export_campaign_passes(
                serializer.validated_data[
                    'campaign'
                ]
            )
        )

        return Response(
            result,
            status=status.HTTP_200_OK
        )
    
class ExportPassPDFAPIView(
    APIView
):

    def post(
        self,
        request
    ):

        serializer = (
            ExportPassPDFSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        service = (
            PassPDFExportService()
        )

        result = (
            service.export_campaign_pdf(
                serializer.validated_data[
                    'campaign'
                ]
            )
        )

        return Response(
            result,
            status=status.HTTP_200_OK
        )