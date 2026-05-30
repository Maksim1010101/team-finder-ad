import re

from django.core.exceptions import ValidationError


def validate_github_url(url):
    pattern = r"^(https?://)?(www\.)?github\.com/[\w\-\.]+(/[\w\-\.]+)+/?$"
    if not re.match(pattern, url):
        raise ValidationError("Введите корректную ссылку на проект ")
