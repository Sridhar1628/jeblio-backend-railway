import qrcode

from io import BytesIO
from django.core.files.base import ContentFile


def generate_qr_code(data, file_name):
    """
    Generate QR code image and return Django ContentFile.
    """

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5,
    )

    qr.add_data(data)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    image.save(buffer, format='PNG')

    return ContentFile(
        buffer.getvalue(),
        name=f"{file_name}.png"
    )