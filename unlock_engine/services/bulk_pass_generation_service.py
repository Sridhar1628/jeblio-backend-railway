from unlock_engine.models.campaign_models import (
    Campaign
)

from unlock_engine.services.pass_generation_service import (
    PassGenerationService
)


class BulkPassGenerationService:

    def __init__(self):

        self.pass_service = (
            PassGenerationService()
        )

    def generate_passes(
        self,
        validated_data
    ):

        campaign_id = validated_data.pop(
            'campaign'
        )

        quantity = validated_data.pop(
            'quantity'
        )

        campaign = Campaign.objects.get(
            id=campaign_id
        )

        generated_passes = []

        for _ in range(quantity):

            pass_data = {
                'campaign': campaign,
                **validated_data
            }

            qr_pass = (
                self.pass_service.create_pass(
                    pass_data
                )
            )

            generated_passes.append(
                qr_pass.id
            )

        campaign.generated_passes += quantity

        if campaign.total_passes < (
            campaign.generated_passes
        ):
            campaign.total_passes = (
                campaign.generated_passes
            )

        campaign.save()

        return {
            "message": (
                f"{quantity} passes "
                f"generated successfully"
            ),
            "generated_count": quantity,
            "campaign": campaign.name
        }