from django.db import models

from unlock_engine.base_models import (
    TimeStampedModel,
    UUIDModel,
    ActiveModel
)

from unlock_engine.choices import (
    PassStatus
)

from unlock_engine.models.campaign_models import Campaign

from django.conf import settings

from unlock_engine.utils.qr_generator import (
    generate_qr_code
)

from unlock_engine.utils.code_generator import (
    generate_pass_code,
    generate_serial_number
)


class Pass(
    UUIDModel,
    TimeStampedModel,
    ActiveModel
):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='passes'
    )

    pass_code = models.CharField(
        max_length=50,
        unique=True
    )

    serial_number = models.CharField(
        max_length=100,
        unique=True
    )

    qr_code_image = models.ImageField(
        upload_to='unlock_engine/qr_codes/',
        blank=True,
        null=True
    )

    qr_data = models.TextField(
        blank=True,
        null=True
    )

    claim_url = models.URLField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=PassStatus.choices,
        default=PassStatus.GENERATED
    )

    expiry_date = models.DateTimeField(
        blank=True,
        null=True
    )

    is_claimed = models.BooleanField(
        default=False
    )

    is_blocked = models.BooleanField(
        default=False
    )

    scan_count = models.PositiveIntegerField(
        default=0
    )

    max_scan_limit = models.PositiveIntegerField(
        default=10
    )

    distribution_source = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    distributed_by = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    distribution_region = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    distribution_college = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    pass_image = models.ImageField(
        upload_to='unlock_engine/passes/',
        blank=True,
        null=True
    )

    pdf_export = models.FileField(
        upload_to='unlock_engine/pdf_exports/',
        blank=True,
        null=True
    )

    template_version = models.CharField(
        max_length=50,
        default="v1"
    )

    first_scanned_at = models.DateTimeField(
        blank=True,
        null=True
    )

    claimed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    converted_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        if not self.pass_code:
            self.pass_code = generate_pass_code()

        if not self.serial_number:
            self.serial_number = generate_serial_number()

        if not self.claim_url:
            self.claim_url = (
                f"{settings.FRONTEND_URL}"
                f"/claim/{self.pass_code}/"
            )

        if not self.qr_code_image and self.claim_url:

            qr_image = generate_qr_code(
                data=self.claim_url,
                file_name=self.pass_code
            )

            self.qr_code_image.save(
                f"{self.pass_code}.png",
                qr_image,
                save=False
            )

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['pass_code']),
            models.Index(fields=['status']),
            models.Index(fields=['distribution_source']),
            models.Index(fields=['distribution_region']),
        ]

    def __str__(self):
        return self.pass_code