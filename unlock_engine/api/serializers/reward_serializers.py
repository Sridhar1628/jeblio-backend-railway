from rest_framework import serializers

from unlock_engine.models.reward_models import Reward
from unlock_engine.api.serializers.base_serializers import (
    BaseModelSerializer
)


class RewardSerializer(BaseModelSerializer):

    campaign_name = serializers.CharField(
        source='campaign.name',
        read_only=True
    )

    class Meta:
        model = Reward
        fields = [
            'id',
            'uuid',
            'campaign',
            'campaign_name',
            'reward_name',
            'reward_code',
            'description',
            'short_description',
            'reward_type',
            'rarity',
            'probability_weight',
            'quantity_limit',
            'remaining_quantity',
            'claimed_quantity',
            'original_value',
            'discount_value',
            'scholarship_percentage',
            'cta_type',
            'cta_url',
            'reward_image',
            'theme_color',
            'status',
            'total_views',
            'total_claims',
            'total_conversions',
            'is_active',
            'created_at',
            'updated_at',
        ]


class CreateRewardSerializer(BaseModelSerializer):

    uuid = None
    created_at = None
    updated_at = None

    class Meta:
        model = Reward
        exclude = [
            'id',
            'uuid',
            'created_at',
            'updated_at',
        ]


class UpdateRewardSerializer(BaseModelSerializer):

    uuid = None
    created_at = None
    updated_at = None

    class Meta:
        model = Reward
        exclude = [
            'id',
            'uuid',
            'reward_code',
            'created_at',
            'updated_at',
        ]