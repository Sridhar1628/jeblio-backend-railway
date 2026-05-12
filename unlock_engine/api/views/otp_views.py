from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from unlock_engine.models.claim_models import Lead
from unlock_engine.models.otp_models import OTPVerification


class VerifyOTPAPIView(APIView):

    def post(self, request):

        lead_id = request.data.get("lead_id")
        otp_code = request.data.get("otp_code")

        try:
            lead = Lead.objects.get(id=lead_id)

        except Lead.DoesNotExist:

            return Response(
                {
                    "error": "Lead not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        otp_record = OTPVerification.objects.filter(
            lead=lead,
            otp_code=otp_code,
            is_verified=False
        ).first()

        if not otp_record:

            return Response(
                {
                    "error": "Invalid OTP"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if otp_record.is_expired():

            return Response(
                {
                    "error": "OTP expired"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        otp_record.is_verified = True
        otp_record.verified_at = timezone.now()
        otp_record.save()

        lead.is_otp_verified = True
        lead.otp_verified_at = timezone.now()
        lead.funnel_stage = "OTP_VERIFIED"
        lead.save()

        return Response(
            {
                "message": "OTP verified successfully"
            },
            status=status.HTTP_200_OK
        )