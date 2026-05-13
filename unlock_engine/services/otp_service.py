from datetime import timedelta

from django.utils import timezone

from unlock_engine.models.otp_models import (
    OTPVerification
)

from unlock_engine.utils.otp_generator import (
    generate_otp_code
)

from jeblioweb_backend.utils.email import (
    send_email
)


class OTPService:

    def send_otp(
        self,
        lead
    ):

        otp_code = (
            generate_otp_code()
        )

        expires_at = (
            timezone.now() +
            timedelta(minutes=10)
        )

        otp_record = (
            OTPVerification.objects.create(
                lead=lead,
                otp_code=otp_code,
                expires_at=expires_at
            )
        )

        subject = (
            "Your Jeblio Verification Code"
        )

        message = f"""
        <div style="
            font-family: Arial, sans-serif;
            background: #000000;
            color: white;
            padding: 40px;
            border-radius: 16px;
        ">

            <h1 style="
                color: #FFD700;
                margin-bottom: 20px;
            ">
                Jeblio Verification
            </h1>

            <p>
                Hello {lead.full_name},
            </p>

            <p>
                Your OTP verification code is:
            </p>

            <div style="
                font-size: 36px;
                font-weight: bold;
                letter-spacing: 8px;
                color: #FFD700;
                margin: 30px 0;
            ">
                {otp_code}
            </div>

            <p>
                This code will expire in
                10 minutes.
            </p>

            <p style="
                margin-top: 40px;
                color: #999999;
                font-size: 12px;
            ">
                © Jeblio — Building Brains.
                Building Brands.
            </p>

        </div>
        """

        send_email(
            to_email=lead.email,
            subject=subject,
            message=message
        )

        return otp_record