import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
from django.conf import settings
from datetime import timedelta, datetime
from certificates.models import Certificate
import base64
import threading

# ✅ IMPORT SENDGRID FUNCTION
from jeblioweb_backend.utils.email import send_email


# ======================
# PATHS
# ======================
BASE_DIR = settings.BASE_DIR

TEMPLATE = os.path.join(BASE_DIR, "media", "template", "certificate_template.png")
OUTPUT = os.path.join(BASE_DIR, "media", "output", "certificates")
QR_FOLDER = os.path.join(BASE_DIR, "media", "qr_codes")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
REPORT_PATH = os.path.join(BASE_DIR, "media", "output", f"email_report_{timestamp}.xlsx")

NAME_FONT_PATH = os.path.join(BASE_DIR, "media", "fonts", "GreatVibes-Regular.ttf")
PARA_FONT_PATH = os.path.join(BASE_DIR, "media", "fonts", "LibreBaskerville-Regular.ttf")
PARA_BOLD_PATH = os.path.join(BASE_DIR, "media", "fonts", "LibreBaskerville-Bold.ttf")


# ======================
# CREATE FOLDERS
# ======================
os.makedirs(OUTPUT, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)


# ======================
# JUSTIFIED TEXT FUNCTION
# ======================
def draw_rich_paragraph(draw, segments, x, y, max_width, line_height):

    words = []
    for text, font in segments:
        for word in text.split(" "):
            words.append((word, font))

    lines = []
    current_line = []
    current_width = 0

    for word, font in words:
        bbox = draw.textbbox((0, 0), word + " ", font=font)
        word_width = bbox[2]

        if current_width + word_width > max_width:
            lines.append(current_line)
            current_line = []
            current_width = 0

        current_line.append((word, font, word_width))
        current_width += word_width

    if current_line:
        lines.append(current_line)

    cursor_y = y

    for i, line in enumerate(lines):
        gaps = len(line) - 1
        line_width = sum(word_width for _, _, word_width in line)

        cursor_x = x

        if i != len(lines) - 1 and gaps > 0:
            extra_space = (max_width - line_width) / gaps
        else:
            extra_space = 0

        for word, font, word_width in line:
            draw.text((cursor_x, cursor_y), word + " ", fill=(0, 0, 0), font=font)
            cursor_x += word_width + extra_space

        cursor_y += line_height


# ======================
# SEND EMAIL WITH ATTACHMENT (SENDGRID)
# ======================
def send_certificate_email(to_email, name, cert_id, verify_url, pdf_path):
    try:
        with open(pdf_path, "rb") as f:
            encoded_file = base64.b64encode(f.read()).decode()

        message = f"""
        <h2>Congratulations {name} 🎉</h2>
        <p>You have successfully completed your internship at <b>Jeblio Corporation Private Limited</b>.</p>

        <p><b>Certificate ID:</b> {cert_id}</p>

        <p>Verify your certificate:</p>
        <a href="{verify_url}">{verify_url}</a>

        <br><br>
        <p>Regards,<br>Jeblio Team</p>
        """

        send_email(
            to_email=to_email,
            subject="Internship Completion Certificate - Jeblio",
            message=message,
            attachment={
                "content": encoded_file,
                "filename": f"{cert_id}.pdf",
                "type": "application/pdf",
                "disposition": "attachment"
            }
        )

    except Exception as e:
        print("Email send failed:", str(e))


# ======================
# MAIN FUNCTION
# ======================
def process_certificates(excel_file_path):

    data = pd.read_excel(excel_file_path)
    data.columns = data.columns.str.lower()

    required_columns = [
        "name", "domain", "project",
        "start_date", "end_date",
        "cert_id", "email"
    ]

    missing = [col for col in required_columns if col not in data.columns]
    if missing:
        raise Exception(f"Missing columns: {missing}")

    report_data = []

    for _, row in data.iterrows():

        qr_path = None
        output_path = None

        try:
            name = str(row["name"])
            domain = str(row["domain"])
            project = str(row["project"])
            email = str(row["email"])

            start_date = pd.to_datetime(row["start_date"]).date()
            end_date = pd.to_datetime(row["end_date"]).date()

            cert_id = str(row["cert_id"])

            start_date_text = start_date.strftime("%d %B %Y")
            end_date_text = end_date.strftime("%d %B %Y")

            issue_date = end_date + timedelta(days=2)
            issue_date_text = issue_date.strftime("%d %B %Y")

            verify_url = f"https://www.jeblio.com/verify/{cert_id}"

            # QR
            qr_path = os.path.join(QR_FOLDER, f"{cert_id}.png")
            qrcode.make(verify_url).save(qr_path)

            # TEMPLATE
            img = Image.open(TEMPLATE).convert("RGB")
            draw = ImageDraw.Draw(img)
            width, height = img.size

            # FONTS
            name_font = ImageFont.truetype(NAME_FONT_PATH, 110)
            paragraph_font = ImageFont.truetype(PARA_FONT_PATH, 38)
            paragraph_bold = ImageFont.truetype(PARA_BOLD_PATH, 38)
            small_font = ImageFont.truetype(PARA_FONT_PATH, 30)

            # NAME
            draw.text((width/2 + 140, 800), name, fill=(184, 134, 11), font=name_font, anchor="mm")

            # PARAGRAPH
            company = "Jeblio Corporation Private Limited"

            segments = [
                ("    This is to certify that", paragraph_font),
                (name, paragraph_bold),
                ("has successfully completed a remote internship at", paragraph_font),
                (company, paragraph_bold),
                (f"from {start_date_text} to {end_date_text} in the domain of", paragraph_font),
                (domain, paragraph_bold),
                ("and successfully completed the project titled", paragraph_font),
                (f"'{project}'.", paragraph_bold)
            ]

            draw_rich_paragraph(draw, segments, width/2 - 440, 960, 1100, 55)

            # CERT ID
            draw.text((width - 650, height - 260), cert_id, fill=(0, 0, 0), font=small_font)
            draw.text((width - 780, height - 215), issue_date_text, fill=(0, 0, 0), font=small_font)

            # QR
            qr_img = Image.open(qr_path).resize((220, 220)).convert("RGB")
            img.paste(qr_img, (width - 260, height - 330))

            # SAVE DB
            Certificate.objects.update_or_create(
                cert_id=cert_id,
                defaults={
                    "name": name,
                    "email": email,
                    "domain": domain,
                    "project": project,
                    "start_date": start_date,
                    "end_date": end_date,
                    "issue_date": issue_date,
                }
            )

            # SAVE PDF
            output_path = os.path.join(OUTPUT, f"{cert_id}.pdf")
            img.save(output_path, "PDF", resolution=300.0)

            # ✅ SEND EMAIL (ASYNC)
            threading.Thread(
                target=send_certificate_email,
                args=(email, name, cert_id, verify_url, output_path)
            ).start()

            status = "SUCCESS"
            error_msg = ""

        except Exception as e:
            status = "FAILED"
            error_msg = str(e)

        report_data.append({
            "name": name,
            "email": email,
            "cert_id": cert_id,
            "status": status,
            "error": error_msg,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    report_df = pd.DataFrame(report_data)
    report_df.to_excel(REPORT_PATH, index=False)

    return REPORT_PATH