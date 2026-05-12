from rest_framework import serializers

from unlock_engine.models.claim_models import Lead
from unlock_engine.api.serializers.base_serializers import (
    BaseModelSerializer
)


class LeadSerializer(BaseModelSerializer):

    campaign_name = serializers.CharField(
        source='campaign.name',
        read_only=True
    )

    assigned_reward_name = serializers.CharField(
        source='assigned_reward.reward_name',
        read_only=True
    )

    pass_code = serializers.CharField(
        source='qr_pass.pass_code',
        read_only=True
    )

    class Meta:
        model = Lead
        fields = [
            'id',
            'uuid',
            'campaign',
            'campaign_name',
            'qr_pass',
            'pass_code',
            'assigned_reward',
            'assigned_reward_name',
            'full_name',
            'email',
            'phone_number',
            'college_name',
            'year_of_study',
            'department',
            'city',
            'is_otp_verified',
            'otp_verified_at',
            'funnel_stage',
            'reward_claimed',
            'consultation_started',
            'payment_completed',
            'scan_time',
            'form_started_at',
            'form_completed_at',
            'reward_claimed_at',
            'converted_at',
            'source_type',
            'source_name',
            'utm_source',
            'utm_campaign',
            'is_active',
            'created_at',
            'updated_at',
        ]


class CreateLeadSerializer(BaseModelSerializer):

    uuid = None
    created_at = None
    updated_at = None

    class Meta:
        model = Lead
        exclude = [
            'id',
            'uuid',
            'assigned_reward',
            'is_otp_verified',
            'otp_verified_at',
            'reward_claimed',
            'consultation_started',
            'payment_completed',
            'reward_claimed_at',
            'converted_at',
            'created_at',
            'updated_at',
        ]


class UpdateLeadSerializer(BaseModelSerializer):

    uuid = None
    created_at = None
    updated_at = None

    class Meta:
        model = Lead
        exclude = [
            'id',
            'uuid',
            'email',
            'phone_number',
            'created_at',
            'updated_at',
        ]