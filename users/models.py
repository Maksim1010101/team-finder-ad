from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
import hashlib
import random
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(email=email, name=name,
                          surname=surname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, name, surname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True, verbose_name="Адрес электронной почты")
    name = models.CharField(max_length=124, verbose_name="Имя")
    surname = models.CharField(max_length=124, verbose_name="Фамилия")
    avatar = models.ImageField(
        upload_to="avatars/",
        default="avatars/default.png",
        verbose_name="Аватар"
    )
    phone = models.CharField(
        max_length=12, null=True, blank=True, verbose_name="Номер телефона"
    )
    github_url = models.URLField(blank=True, verbose_name="Ссылка на GitHub")
    about = models.TextField(blank=True, max_length=256, verbose_name="О себе")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    favorites = models.ManyToManyField(
        "projects.Project",
        blank=True,
        related_name="favorited_by",
        verbose_name="Избранные проекты",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.name} {self.surname}"

    def save(self, *args, **kwargs):
        if not self.avatar or self.avatar.name == "avatars/default.png":
            self.avatar = self._generate_avatar()
        super().save(*args, **kwargs)

    def _generate_avatar(self):
        size = (200, 200)
        color = self._random_pastel_color()
        image = Image.new("RGB", size, color)
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", 100)
        except Exception:
            font = ImageFont.load_default()
        letter = self.name[0].upper()
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
        draw.text(position, letter, fill="white", font=font)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        filename = f"avatar_{hashlib.md5(self.email.encode()).hexdigest()}.png"
        return ContentFile(buffer.getvalue(), name=filename)

    @staticmethod
    def _random_pastel_color():
        r = random.randint(120, 200)
        g = random.randint(120, 200)
        b = random.randint(120, 200)
        return (r, g, b)
