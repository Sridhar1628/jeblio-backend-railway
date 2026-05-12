from django.db import models

from unlock_engine.base_models import (
    TimeStampedModel,
    UUIDModel,
    ActiveModel
)

from unlock_engine.models.campaign_models import Campaign
from unlock_engine.models.pass_models import Pass
from unlock_engine.models.reward_models import Reward


class Lead(
    UUIDModel,
    TimeStampedModel,
    ActiveModel
):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='leads'
    )

    qr_pass = models.ForeignKey(
        Pass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads'
    )

    assigned_reward = models.ForeignKey(
        Reward,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads'
    )

    full_name = models.CharField(
        max_length=255
    )

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=20
    )

    college_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    year_of_study = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    department = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    is_otp_verified = models.BooleanField(
        default=False
    )

    otp_verified_at = models.DateTimeField(
        blank=True,
        null=True
    )

    funnel_stage = models.CharField(
        max_length=50,
        default="SCANNED"
    )

    reward_claimed = models.BooleanField(
        default=False
    )

    consultation_started = models.BooleanField(
        default=False
    )

    payment_completed = models.BooleanField(
        default=False
    )

    scan_time = models.DateTimeField(
        blank=True,
        null=True
    )

    form_started_at = models.DateTimeField(
        blank=True,
        null=True
    )

    form_completed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    reward_claimed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    converted_at = models.DateTimeField(
        blank=True,
        null=True
    )

    source_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    source_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    utm_source = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    utm_campaign = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['funnel_stage']),
            models.Index(fields=['is_otp_verified']),
        ]

    def __str__(self):
        return self.full_name