from rest_framework import serializers

from unlock_engine.models.pass_models import Pass
from unlock_engine.api.serializers.base_serializers import (
    BaseModelSerializer
)


class PassSerializer(BaseModelSerializer):

    campaign_name = serializers.CharField(
        source='campaign.name',
        read_only=True
    )

    class Meta:
        model = Pass
        fields = [
            'id',
            'uuid',
            'campaign',
            'campaign_name',
            'pass_code',
            'serial_number',
            'qr_code_image',
            'qr_data',
            'claim_url',
            'status',
            'expiry_date',
            'is_claimed',
            'is_blocked',
            'scan_count',
            'max_scan_limit',
            'distribution_source',
            'distributed_by',
            'distribution_region',
            'distribution_college',
            'pass_image',
            'pdf_export',
            'template_version',
            'first_scanned_at',
            'claimed_at',
            'converted_at',
            'is_active',
            'created_at',
            'updated_at',
        ]


class CreatePassSerializer(BaseModelSerializer):

    uuid = None
    created_at = None
    updated_at = None

    class Meta:
        model = Pass
        exclude = [
            'id',
            'uuid',
            'pass_code',
            'serial_number',
            'qr_code_image',
            'qr_data',
            'claim_url',
            'created_at',
            'updated_at',
        ]


class UpdatePassSerializer(BaseModelSerializer):

    uuid = None
    created_at = None
    updated_at = None

    class Meta:
        model = Pass
        exclude = [
            'id',
            'uuid',
            'pass_code',
            'serial_number',
            'created_at',
            'updated_at',
        ]