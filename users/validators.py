import re

from django.core.exceptions import ValidationError


def validate_github_url(url):
    pattern = r"^(https?://)?(www\.)?github\.com/[\w\-\.]+/?$"
    if not re.match(pattern, url):
        raise ValidationError("Введите корректную ссылку на ваш профиль")


def validate_phone_number(phone):
    if not re.search(r"(^8\d{10}$)|(^\+7\d{10}$)", phone):
        raise ValidationError("Введите правильный номер телефона")
