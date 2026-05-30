import hashlib
import random
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont


def random_pastel_color():
    r = random.randint(120, 200)
    g = random.randint(120, 200)
    b = random.randint(120, 200)
    return (r, g, b)


def generate_avatar(name, email):
    size = (200, 200)
    color = random_pastel_color()
    image = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except Exception:
        font = ImageFont.load_default()
    letter = name[0].upper()
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    draw.text(position, letter, fill='white', font=font)
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    filename = f'avatar_{hashlib.md5(email.encode()).hexdigest()}.png'
    return ContentFile(buffer.getvalue(), name=filename)
