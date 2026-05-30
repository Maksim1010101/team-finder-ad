from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from users.managers import UserManager
from users.utils import generate_avatar
from core.constants import MAX_NAME_LEN, MAX_SURNAME_LEN, MAX_ABOUT_LEN, MAX_PHONE_LEN


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True, verbose_name="Адрес электронной почты")
    name = models.CharField(max_length=MAX_NAME_LEN, verbose_name="Имя")
    surname = models.CharField(
        max_length=MAX_SURNAME_LEN, verbose_name="Фамилия")
    avatar = models.ImageField(
        upload_to="avatars/",
        default="avatars/default.png",
        verbose_name="Аватар"
    )
    phone = models.CharField(
        max_length=MAX_PHONE_LEN, null=True, blank=True, verbose_name="Номер телефона"
    )
    github_url = models.URLField(blank=True, verbose_name="Ссылка на GitHub")
    about = models.TextField(
        blank=True, max_length=MAX_ABOUT_LEN, verbose_name="О себе")
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
        if not self.avatar or self.avatar.name == 'avatars/default.png':
            self.avatar = generate_avatar(self.name, self.email)
        super().save(*args, **kwargs)
