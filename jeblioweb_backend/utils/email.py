import os
import logging

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition
)

logger = logging.getLogger(__name__)


def send_email(to_email, subject, message, attachment=None):

    try:

        api_key = os.getenv("SENDGRID_API_KEY")

        if not api_key:
            logger.error("SENDGRID_API_KEY not found")
            return False

        sg = SendGridAPIClient(api_key)

        email = Mail(
            from_email="jeblioinfo@gmail.com",
            to_emails=to_email,
            subject=subject,
            html_content=message
        )

        # ======================
        # ATTACHMENT SUPPORT
        # ======================

        if attachment:

            attached_file = Attachment(
                FileContent(attachment["content"]),
                FileName(attachment["filename"]),
                FileType(attachment["type"]),
                Disposition(attachment["disposition"])
            )

            email.attachment = attached_file

        # ======================
        # SEND EMAIL
        # ======================

        response = sg.send(email)

        logger.info(
            f"Email sent successfully to {to_email} | Status: {response.status_code}"
        )

        print("✅ EMAIL SENT")
        print("STATUS CODE:", response.status_code)

        return True

    except Exception as e:

        logger.exception("SENDGRID EMAIL ERROR")

        print("❌ EMAIL ERROR:", str(e))

        return False