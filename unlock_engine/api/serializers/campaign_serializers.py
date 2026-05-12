from rest_framework import serializers

from unlock_engine.models.campaign_models import Campaign
from unlock_engine.api.serializers.base_serializers import (
    BaseModelSerializer
)


class CampaignSerializer(BaseModelSerializer):

    class Meta:
        model = Campaign
        fields = [
            'id',
            'uuid',
            'name',
            'slug',
            'description',
            'campaign_code',
            'campaign_type',
            'status',
            'start_date',
            'end_date',
            'expiry_date',
            'total_passes',
            'generated_passes',
            'claimed_passes',
            'total_scans',
            'total_claims',
            'total_conversions',
            'distribution_source',
            'influencer_name',
            'region',
            'banner_image',
            'theme_color',
            'is_active',
            'created_at',
            'updated_at',
        ]


class CreateCampaignSerializer(BaseModelSerializer):

    uuid = None
    created_at = None
    updated_at = None


    class Meta:
        model = Campaign
        exclude = [
            'id',
            'uuid',
            'slug',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['uuid']


class UpdateCampaignSerializer(BaseModelSerializer):

    uuid = None
    created_at = None
    updated_at = None


    class Meta:
        model = Campaign
        exclude = [
            'id',
            'uuid',
            'campaign_code',
            'created_at',
            'updated_at',
        ]