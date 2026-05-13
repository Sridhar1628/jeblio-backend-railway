from django.utils import timezone

from rest_framework import generics, status
from rest_framework.response import Response

from unlock_engine.api.serializers.reward_serializers import RewardSerializer
from unlock_engine.models.claim_models import Lead
from unlock_engine.models.pass_models import Pass

from unlock_engine.api.serializers.lead_serializers import (
    LeadSerializer,
    CreateLeadSerializer,
    UpdateLeadSerializer
)

from unlock_engine.utils.scan_tracker import (
    track_pass_scan
)

from unlock_engine.services.otp_service import (
    OTPService
)

from rest_framework.views import APIView

from unlock_engine.utils.reward_engine import (
    assign_reward
)


class LeadListCreateAPIView(
    generics.ListCreateAPIView
):
    queryset = Lead.objects.all().order_by('-created_at')

    def get_serializer_class(self):

        if self.request.method == 'POST':
            return CreateLeadSerializer

        return LeadSerializer

    def create(self, request, *args, **kwargs):

        pass_id = request.data.get('qr_pass')

        try:
            qr_pass = Pass.objects.get(id=pass_id)

        except Pass.DoesNotExist:
            return Response(
                {
                    "error": "Invalid pass selected"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if qr_pass.is_blocked:
            return Response(
                {
                    "error": "This pass is blocked"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if qr_pass.is_claimed:
            return Response(
                {
                    "error": "This pass is already claimed"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        existing_lead = Lead.objects.filter(
            email=request.data.get('email'),
            qr_pass=qr_pass
        ).first()

        if existing_lead:

            return Response(
                {
                    "error": (
                        "Lead already registered "
                        "with this pass"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        lead = serializer.save(
            scan_time=timezone.now(),
            funnel_stage="FORM_STARTED"
        )

        track_pass_scan(qr_pass)

        # =========================
        # SEND OTP
        # =========================

        otp_service = OTPService()

        otp_service.send_otp(
            lead
        )

        return Response(
            LeadSerializer(lead).data,
            status=status.HTTP_201_CREATED
        )


class LeadRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Lead.objects.all()

    def get_serializer_class(self):

        if self.request.method in ['PUT', 'PATCH']:
            return UpdateLeadSerializer

        return LeadSerializer
    
class ClaimRewardAPIView(APIView):

    def post(self, request, pk):

        try:
            lead = Lead.objects.get(pk=pk)

        except Lead.DoesNotExist:

            return Response(
                {
                    "error": "Lead not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if lead.reward_claimed:

            return Response(
                {
                    "error": "Reward already claimed"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not lead.is_otp_verified:

            return Response(
                {
                    "error": (
                        "OTP verification required"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not lead.campaign.is_active:

            return Response(
                {
                    "error": (
                        "Campaign is inactive"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # =========================
        # CAMPAIGN EXPIRY CHECK
        # =========================

        campaign = lead.campaign

        if (
            campaign.expiry_date and
            campaign.expiry_date < timezone.now()
        ):

            return Response(
                {
                    "error": (
                        "This campaign has expired"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # =========================
        # PASS CLAIM RECHECK
        # =========================

        qr_pass = lead.qr_pass

        if qr_pass and qr_pass.is_claimed:

            return Response(
                {
                    "error": (
                        "This pass has already "
                        "been claimed"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        reward = assign_reward(lead.campaign)

        if not reward:

            return Response(
                {
                    "error": "No rewards available"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        lead.assigned_reward = reward
        lead.reward_claimed = True
        lead.funnel_stage = "CLAIMED"
        lead.reward_claimed_at = timezone.now()

        lead.save()

        qr_pass = lead.qr_pass

        if qr_pass:
            qr_pass.is_claimed = True
            qr_pass.claimed_at = timezone.now()
            qr_pass.save()

        campaign = lead.campaign
        campaign.total_claims += 1
        campaign.save()

        return Response(
            {
                "message": "Reward claimed successfully",
                "reward": RewardSerializer(reward).data
            },
            status=status.HTTP_200_OK
        )