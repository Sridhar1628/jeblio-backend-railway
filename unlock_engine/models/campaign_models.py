from django.db import models
from django.utils.text import slugify

from unlock_engine.base_models import (
    TimeStampedModel,
    UUIDModel,
    ActiveModel
)

from unlock_engine.choices import (
    CampaignType,
    CampaignStatus
)


class Campaign(
    UUIDModel,
    TimeStampedModel,
    ActiveModel
):
    name = models.CharField(
        max_length=255,
        unique=True
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    campaign_code = models.CharField(
        max_length=50,
        unique=True
    )

    campaign_type = models.CharField(
        max_length=50,
        choices=CampaignType.choices,
        default=CampaignType.WORKSHOP
    )

    status = models.CharField(
        max_length=20,
        choices=CampaignStatus.choices,
        default=CampaignStatus.DRAFT
    )

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    expiry_date = models.DateTimeField(
        blank=True,
        null=True
    )

    total_passes = models.PositiveIntegerField(
        default=0
    )

    generated_passes = models.PositiveIntegerField(
        default=0
    )

    claimed_passes = models.PositiveIntegerField(
        default=0
    )

    total_scans = models.PositiveIntegerField(
        default=0
    )

    total_claims = models.PositiveIntegerField(
        default=0
    )

    total_conversions = models.PositiveIntegerField(
        default=0
    )

    distribution_source = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    influencer_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    region = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    banner_image = models.ImageField(
        upload_to='unlock_engine/campaigns/banners/',
        blank=True,
        null=True
    )

    theme_color = models.CharField(
        max_length=20,
        default="#000000"
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['campaign_code']),
            models.Index(fields=['status']),
            models.Index(fields=['campaign_type']),
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name