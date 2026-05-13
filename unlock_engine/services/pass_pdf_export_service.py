import os

from django.conf import settings

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from unlock_engine.models.pass_models import (
    Pass
)

from unlock_engine.models.campaign_models import (
    Campaign
)


class PassPDFExportService:

    def export_campaign_pdf(
        self,
        campaign_id
    ):

        campaign = Campaign.objects.get(
            id=campaign_id
        )

        passes = Pass.objects.filter(
            campaign=campaign
        )

        export_dir = os.path.join(
            settings.MEDIA_ROOT,
            'unlock_engine',
            'pdf_exports'
        )

        os.makedirs(
            export_dir,
            exist_ok=True
        )

        pdf_file_name = (
            f"{campaign.campaign_code}_passes.pdf"
        )

        pdf_file_path = os.path.join(
            export_dir,
            pdf_file_name
        )

        pdf = canvas.Canvas(
            pdf_file_path,
            pagesize=A4
        )

        page_width, page_height = A4

        card_width = 500
        card_height = 280

        positions = [
            (50, page_height - 330),
            (50, page_height - 650),
        ]

        position_index = 0

        for qr_pass in passes:

            if not qr_pass.pass_image:
                continue

            image_path = (
                qr_pass.pass_image.path
            )

            x, y = positions[
                position_index
            ]

            pdf.drawImage(
                image_path,
                x,
                y,
                width=card_width,
                height=card_height,
                preserveAspectRatio=True,
                mask='auto'
            )

            position_index += 1

            if position_index >= 2:

                pdf.showPage()

                position_index = 0

        if position_index != 0:
            pdf.showPage()

        pdf.save()

        pdf_url = (
            f"{settings.FRONTEND_URL}"
            f"{settings.MEDIA_URL}"
            f"unlock_engine/pdf_exports/"
            f"{pdf_file_name}"
        )

        return {
            "message": (
                "PDF export generated "
                "successfully"
            ),
            "campaign": campaign.name,
            "pdf_url": pdf_url
        }