from django.db import models

from unlock_engine.base_models import (
    TimeStampedModel,
    UUIDModel,
    ActiveModel
)

from unlock_engine.choices import (
    RewardType,
    RewardRarity,
    CampaignStatus
)

from unlock_engine.models.campaign_models import Campaign


class Reward(
    UUIDModel,
    TimeStampedModel,
    ActiveModel
):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='rewards'
    )

    reward_name = models.CharField(
        max_length=255
    )

    reward_code = models.CharField(
        max_length=50,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    short_description = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    reward_type = models.CharField(
        max_length=50,
        choices=RewardType.choices,
        default=RewardType.WORKSHOP
    )

    rarity = models.CharField(
        max_length=20,
        choices=RewardRarity.choices,
        default=RewardRarity.COMMON
    )

    probability_weight = models.PositiveIntegerField(
        default=1
    )

    quantity_limit = models.PositiveIntegerField(
        default=0
    )

    remaining_quantity = models.PositiveIntegerField(
        default=0
    )

    claimed_quantity = models.PositiveIntegerField(
        default=0
    )

    original_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    scholarship_percentage = models.PositiveIntegerField(
        default=0
    )

    cta_type = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    cta_url = models.URLField(
        blank=True,
        null=True
    )

    reward_image = models.ImageField(
        upload_to='unlock_engine/rewards/',
        blank=True,
        null=True
    )

    theme_color = models.CharField(
        max_length=20,
        default="#FFD700"
    )

    status = models.CharField(
        max_length=20,
        choices=CampaignStatus.choices,
        default=CampaignStatus.ACTIVE
    )

    total_views = models.PositiveIntegerField(
        default=0
    )

    total_claims = models.PositiveIntegerField(
        default=0
    )

    total_conversions = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reward_code']),
            models.Index(fields=['reward_type']),
            models.Index(fields=['rarity']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.reward_name