from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    """Model of task in project."""

    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        verbose_name=_("Name"),
    )

    description = models.TextField(
        max_length=25500,
        blank=True,
        verbose_name=_("Description"),
    )

    status = models.ForeignKey(
        to=Status,
        on_delete=models.RESTRICT,
        verbose_name=_("Status"),
    )

    author = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        verbose_name=_("Author"),
        related_name="author",
    )

    performer = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        verbose_name=_("Performer"),
        related_name="performer",
    )

    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Creation date")
    )