from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    """Label (Tag) model of project."""

    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        verbose_name=_("Name")
    )

    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Creation date")
    )

    objects = models.Manager()

    def __str__(self):
        return self.name
