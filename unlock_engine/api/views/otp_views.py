from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from unlock_engine.models.claim_models import Lead
from unlock_engine.models.otp_models import OTPVerification


class VerifyOTPAPIView(APIView):

    def post(self, request):

        try:

            lead_id = request.data.get("lead_id")
            otp_code = request.data.get("otp_code")

            # =========================
            # VALIDATION
            # =========================

            if not lead_id or not otp_code:

                return Response(
                    {
                        "error": "Lead ID and OTP are required"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # =========================
            # GET LEAD
            # =========================

            try:

                lead = Lead.objects.get(id=lead_id)

            except Lead.DoesNotExist:

                return Response(
                    {
                        "error": "Lead not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # =========================
            # GET LATEST OTP
            # =========================

            otp_record = OTPVerification.objects.filter(
                lead=lead,
                is_verified=False
            ).order_by("-created_at").first()

            if not otp_record:

                return Response(
                    {
                        "error": "No OTP found"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # =========================
            # CHECK EXPIRY
            # =========================

            if otp_record.is_expired():

                return Response(
                    {
                        "error": "OTP expired"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # =========================
            # CHECK OTP MATCH
            # =========================

            if otp_record.otp_code != otp_code:

                otp_record.attempt_count += 1
                otp_record.save()

                return Response(
                    {
                        "error": "Invalid OTP"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # =========================
            # SUCCESS
            # =========================

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

        except Exception as e:

            print("OTP VERIFY ERROR:", str(e))

            return Response(
                {
                    "error": "Something went wrong"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )