
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.managers import IsDeletedModel

__all__ = (
    'AppointmentsArchive',
    'Appointments',
)


class BaseAppointmentsClass(IsDeletedModel):
    date = models.DateField(verbose_name=_('Appointment date'))
    time = models.DateTimeField(verbose_name=_('Appointment time'))
    duration = models.PositiveIntegerField(verbose_name=_('Appointment duration (seconds)'))
    workman = models.ForeignKey("Workman", verbose_name=_("Repair mechanic"), on_delete=models.CASCADE)
    customer = models.ForeignKey("User", verbose_name=_("Customer"), on_delete=models.CASCADE)
    work_regime = models.ForeignKey("WorkRegime", verbose_name=_("Work regime"), on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        workman = self.workman.get_full_name()
        customer = self.customer.get_full_name()
        date_format = '%Y/%m/%d %H:%M'

        return f"{self.time.strftime(date_format)} ({customer} -> {workman})"


class AppointmentsArchive(BaseAppointmentsClass):

    class Meta:
        verbose_name = _('Appointment (archive)')
        verbose_name_plural = _('Appointments (archive)')


class Appointments(BaseAppointmentsClass):

    class Meta:
        verbose_name = _('Appointment')
        verbose_name_plural = _('Appointments')
