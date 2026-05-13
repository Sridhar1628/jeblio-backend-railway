import os
import zipfile

from django.conf import settings

from unlock_engine.models.pass_models import (
    Pass
)

from unlock_engine.models.campaign_models import (
    Campaign
)


class PassZipExportService:

    def export_campaign_passes(
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
            'zip_exports'
        )

        os.makedirs(
            export_dir,
            exist_ok=True
        )

        zip_file_name = (
            f"{campaign.campaign_code}_passes.zip"
        )

        zip_file_path = os.path.join(
            export_dir,
            zip_file_name
        )

        with zipfile.ZipFile(
            zip_file_path,
            'w',
            zipfile.ZIP_DEFLATED
        ) as zipf:

            for qr_pass in passes:

                if qr_pass.pass_image:

                    image_path = (
                        qr_pass.pass_image.path
                    )

                    zipf.write(
                        image_path,
                        arcname=os.path.basename(
                            image_path
                        )
                    )

        zip_url = (
            f"{settings.FRONTEND_URL}"
            f"{settings.MEDIA_URL}"
            f"unlock_engine/zip_exports/"
            f"{zip_file_name}"
        )

        return {
            "message": (
                "ZIP export generated "
                "successfully"
            ),
            "campaign": campaign.name,
            "zip_url": zip_url
        }