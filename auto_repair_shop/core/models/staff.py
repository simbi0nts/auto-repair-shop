
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.managers import IsDeletedModel

__all__ = (
    'Workman',
)


class Workman(IsDeletedModel):
    first_name = models.CharField(max_length=128, verbose_name=_('First name'))
    middle_name = models.CharField(max_length=128, verbose_name=_('Middle name'), null=True, blank=True)
    last_name = models.CharField(max_length=128, verbose_name=_('Last Name'))

    repair_shop = models.ForeignKey("RepairShop", verbose_name=_("Repair shop"), on_delete=models.PROTECT)
    individual_work_regime = models.ForeignKey("WorkRegime", verbose_name=_("Individual work regime (optional)"),
                                               null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('last_name', 'first_name', 'middle_name',)
        verbose_name = _('Workman')
        verbose_name_plural = _('Workmans')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self) -> str:
        m_n = self.middle_name or ""
        return "%s %s %s" % tuple(x.capitalize() for x in (self.last_name, self.first_name, m_n))
