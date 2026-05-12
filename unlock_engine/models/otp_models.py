from django.db import models
from django.utils import timezone

from unlock_engine.base_models import (
    TimeStampedModel,
    UUIDModel
)

from unlock_engine.models.claim_models import Lead


class OTPVerification(
    UUIDModel,
    TimeStampedModel
):
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='otp_verifications'
    )

    otp_code = models.CharField(
        max_length=6
    )

    is_verified = models.BooleanField(
        default=False
    )

    expires_at = models.DateTimeField()

    verified_at = models.DateTimeField(
        blank=True,
        null=True
    )

    attempt_count = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['-created_at']

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.lead.full_name} - {self.otp_code}"