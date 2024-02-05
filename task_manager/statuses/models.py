from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    """Status model"""
    name = models.CharField(max_length=255,
                            unique=True,
                            blank=False,
                            verbose_name=_('Name'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Creation date'))
    objects = models.Manager()

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')
