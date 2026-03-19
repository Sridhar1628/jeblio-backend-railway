from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import os
import traceback

from .utils import process_certificates


class UploadExcelView(APIView):

    def post(self, request):
        try:
            file = request.FILES.get("file")

            # ======================
            # VALIDATION
            # ======================
            if not file:
                return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

            if not file.name.endswith((".xlsx", ".xls")):
                return Response({"error": "Only Excel files are allowed"}, status=status.HTTP_400_BAD_REQUEST)

            # ======================
            # SAVE FILE TO MEDIA
            # ======================
            upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
            os.makedirs(upload_dir, exist_ok=True)

            file_path = os.path.join(upload_dir, file.name)

            with open(file_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # ======================
            # PROCESS CERTIFICATES
            # ======================
            report_path = process_certificates(file_path)

            # ======================
            # RETURN RESPONSE
            # ======================
            return Response({
                "message": "Certificates processed successfully",
                "report_file": report_path
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print("\n🔥 FULL ERROR BELOW 🔥")
            traceback.print_exc()

            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
from django.http import FileResponse
import os

class DownloadReportView(APIView):

    def get(self, request):
        file_path = request.GET.get("path")

        if not file_path or not os.path.exists(file_path):
            return Response({"error": "File not found"}, status=404)

        return FileResponse(open(file_path, "rb"), as_attachment=True)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Certificate
from .serializers import CertificateSerializer


class CertificateVerifyView(APIView):

    def get(self, request, cert_id):
        try:
            certificate = Certificate.objects.get(cert_id=cert_id)
            serializer = CertificateSerializer(certificate)

            return Response({
                "status": "valid",
                "data": serializer.data
            })

        except Certificate.DoesNotExist:
            return Response({
                "status": "invalid",
                "message": "Certificate not found"
            }, status=status.HTTP_404_NOT_FOUND)