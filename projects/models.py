from core.constants import MAX_PROJECT_LEN_NAME
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Project(models.Model):
    OPEN = "open"
    CLOSED = "closed"

    STATUS_CHOICES = [
        (OPEN, "Open"),
        (CLOSED, "Closed"),
    ]
    name = models.CharField(max_length=MAX_PROJECT_LEN_NAME,
                            verbose_name="Название проекта")
    description = models.TextField(blank=True, verbose_name="Описание проекта")
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Владелец проекта",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")
    github_url = models.URLField(blank=True, verbose_name="Ссылка на GitHub")
    status = models.CharField(
        max_length=6,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0],
        verbose_name="Статус проекта",
    )
    participants = models.ManyToManyField(
        User,
        blank=True,
        verbose_name="Участники проекта",
        related_name="participated_projects",
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name
