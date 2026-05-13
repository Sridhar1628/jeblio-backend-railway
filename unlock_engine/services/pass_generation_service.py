import os

from django.conf import settings
from django.core.files import File

from unlock_engine.models.pass_models import Pass
from unlock_engine.services.card_generator import (
    SmartCardGenerator
)


class PassGenerationService:

    def __init__(self):

        self.card_generator = (
            SmartCardGenerator()
        )

    def generate_pass_card(
        self,
        qr_pass
    ):

        template, draw = (
            self.card_generator.prepare_canvas()
        )

        qr_image = (
            self.card_generator.generate_qr_code(
                qr_pass.claim_url
            )
        )

        self.card_generator.add_qr_to_template(
            template,
            qr_image
        )

        self.card_generator.add_pass_code(
            draw,
            qr_pass.pass_code
        )

        valid_date = (
            qr_pass.expiry_date.strftime(
                "%d %b %Y"
            ).upper()
            if qr_pass.expiry_date
            else "NO EXPIRY"
        )

        self.card_generator.add_valid_date(
            draw,
            valid_date
        )

        output_dir = os.path.join(
            settings.MEDIA_ROOT,
            "generated_passes"
        )

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        file_name = (
            f"{qr_pass.pass_code}.png"
        )

        output_path = os.path.join(
            output_dir,
            file_name
        )

        template.save(output_path)

        with open(output_path, "rb") as image_file:

            qr_pass.pass_image.save(
                file_name,
                File(image_file),
                save=False
            )

        qr_pass.save()

        return qr_pass

    def create_pass(
        self,
        validated_data
    ):

        qr_pass = Pass.objects.create(
            **validated_data
        )

        self.generate_pass_card(
            qr_pass
        )

        return qr_pass