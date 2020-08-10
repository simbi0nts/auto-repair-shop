
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.managers import IsDeletedModel

__all__ = (
    'RepairShop',
)


class RepairShop(IsDeletedModel):
    name = models.CharField(max_length=128, verbose_name=_("Repair shop name"))  # unique=True (?)
    default_work_regime = models.ForeignKey("WorkRegime", verbose_name=_("Default work regime (optional)"),
                                            null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Repair shop')
        verbose_name_plural = _('Repair shops')

    def __str__(self):
        return self.name or ""
