import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition
)


def send_email(to_email, subject, message, attachment=None):
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

        email = Mail(
            from_email='no-reply@jeblio.com',  # must be verified in SendGrid
            to_emails=to_email,
            subject=subject,
            html_content=message
        )

        # ======================
        # ATTACHMENT SUPPORT
        # ======================
        if attachment:
            attached_file = Attachment(
                FileContent(attachment["content"]),   # base64 encoded
                FileName(attachment["filename"]),
                FileType(attachment["type"]),
                Disposition(attachment["disposition"])
            )
            email.attachment = attached_file   # IMPORTANT

        # ======================
        # SEND EMAIL
        # ======================
        response = sg.send(email)

        print("✅ Email sent:", response.status_code)

    except Exception as e:
        print("❌ Email failed:", str(e))