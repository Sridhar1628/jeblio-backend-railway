from PIL import (
    Image,
    ImageDraw,
    ImageFont
)

import qrcode


class SmartCardGenerator:

    def __init__(self):

        self.template_path = (
            "media/card_templates/"
            "exclusive-pass-template.png"
        )

        self.font_path = (
            "C:/Windows/Fonts/arial.ttf"
        )

        self.bold_font_path = (
            "C:/Windows/Fonts/arialbd.ttf"
        )

    def load_template(self):

        return Image.open(
            self.template_path
        ).convert("RGBA")

    def prepare_canvas(self):

        template = self.load_template()

        draw = ImageDraw.Draw(template)

        return template, draw

    def center_text(
        self,
        draw,
        text,
        font,
        box_x,
        box_y,
        box_width,
        box_height
    ):

        bbox = draw.textbbox(
            (0, 0),
            text,
            font=font
        )

        text_width = (
            bbox[2] - bbox[0]
        )

        text_height = (
            bbox[3] - bbox[1]
        )

        x = (
            box_x +
            (box_width - text_width) / 2
        )

        y = (
            box_y +
            (box_height - text_height) / 2
        )

        return x, y

    def generate_qr_code(
        self,
        qr_data
    ):

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=2
        )

        qr.add_data(
            qr_data
        )

        qr.make(
            fit=True
        )

        qr_image = qr.make_image(
            fill_color="black",
            back_color="white"
        ).convert("RGBA")

        qr_image = qr_image.resize(
            (272, 272)
        )

        return qr_image

    def add_qr_to_template(
        self,
        template,
        qr_image
    ):

        qr_x = 1174
        qr_y = 182

        template.paste(
            qr_image,
            (qr_x, qr_y),
            qr_image
        )

    def add_pass_code(
        self,
        draw,
        pass_code
    ):

        font = ImageFont.truetype(
            self.bold_font_path,
            30
        )

        box_x = 1130
        box_y = 490
        box_width = 360
        box_height = 55

        x, y = self.center_text(
            draw,
            pass_code,
            font,
            box_x,
            box_y,
            box_width,
            box_height
        )

        draw.text(
            (x, y),
            pass_code,
            fill=(255, 215, 0),
            font=font
        )

    def add_valid_date(
        self,
        draw,
        valid_date
    ):

        font = ImageFont.truetype(
            self.bold_font_path,
            24
        )

        box_x = 1160
        box_y = 570
        box_width = 300
        box_height = 40

        x, y = self.center_text(
            draw,
            valid_date,
            font,
            box_x,
            box_y,
            box_width,
            box_height
        )

        draw.text(
            (x, y),
            valid_date,
            fill=(255, 230, 120),
            font=font
        )

    def save_card(
        self,
        template,
        output_path
    ):

        template.save(
            output_path
        )

    def generate_demo_card(self):

        template, draw = (
            self.prepare_canvas()
        )

        pass_code = (
            "JB26-X9Q7-K3L8"
        )

        qr_url = (
            f"https://jeblio.com/claim?"
            f"code={pass_code}"
        )

        qr_image = self.generate_qr_code(
            qr_url
        )

        self.add_qr_to_template(
            template,
            qr_image
        )

        self.add_pass_code(
            draw,
            pass_code
        )

        self.add_valid_date(
            draw,
            "31 DEC 2026"
        )

        output_path = (
            "media/generated_cards/"
            "demo_card.png"
        )

        self.save_card(
            template,
            output_path
        )

        return output_path