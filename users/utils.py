import hashlib
import random
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from core.constants import (
    AVATAR_FONT_SIZE,
    AVATAR_SIZE,
    AVATAR_TEXT_COLOR,
    BBOX_COORDINATES,
    FONT_PATHS,
)


def random_pastel_color():
    return tuple(random.randint(120, 200) for _ in range(3))


def get_font(size):
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


def generate_avatar(name, email, size=None, text_color=None):
    size = AVATAR_SIZE
    text_color = AVATAR_TEXT_COLOR
    color = random_pastel_color()
    image = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(image)
    font = get_font(AVATAR_FONT_SIZE)
    letter = name[0].upper()
    bbox = draw.textbbox(BBOX_COORDINATES, letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    draw.text(position, letter, fill=text_color, font=font)

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    filename = f"avatar_{hashlib.md5(email.encode()).hexdigest()}.png"
    return ContentFile(buffer.getvalue(), name=filename)
