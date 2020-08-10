
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.managers import IsDeletedModel

__all__ = (
    'WorkRegime',
    'WorkRegimeExceptions',
    'WorkRegimeDetail'
)


class DaysOfTheWeek(dict):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


DAYS_OF_THE_WEEK = DaysOfTheWeek({
    DaysOfTheWeek.MONDAY: _("Monday"),
    DaysOfTheWeek.TUESDAY: _("Tuesday"),
    DaysOfTheWeek.WEDNESDAY: _("Wednesday"),
    DaysOfTheWeek.THURSDAY: _("Thursday"),
    DaysOfTheWeek.FRIDAY: _("Friday"),
    DaysOfTheWeek.SATURDAY: _("Saturday"),
    DaysOfTheWeek.SUNDAY: _("Sunday"),
})


class WorkRegime(IsDeletedModel):
    name = models.CharField(max_length=128, verbose_name=_("Regime name"))
    repair_shop = models.ForeignKey("RepairShop", verbose_name=_("Repair shop"), on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('Work regime')
        verbose_name_plural = _('Work regimes')

    def __str__(self):
        return self.name

    def _get_wrd_exception(self, date):
        try:
            return WorkRegimeExceptions.objects.get(
                work_regime__id=self.id,
                date=date
            )
        except ObjectDoesNotExist:
            return None

    def get_wrd(self, date, is_exception=False):
        if is_exception:
            return self._get_wrd_exception(date)

        try:
            return WorkRegimeDetail.objects.get(
                work_regime__id=self.id,
                day_of_week=date.weekday()
            )
        except ObjectDoesNotExist:
            return None


def get_work_time_args(is_work_time_optional: bool) -> dict:
    _d = {}
    if is_work_time_optional:
        _d.update({"null": True, "blank": True})
    return _d


class BaseWorkRegimeDetails(IsDeletedModel):
    IS_WORK_TIME_OPTIONAL = False
    work_time_args = get_work_time_args(IS_WORK_TIME_OPTIONAL)

    work_regime = models.ForeignKey("WorkRegime", verbose_name=_("Regime"), on_delete=models.PROTECT)
    work_time_begin = models.TimeField(verbose_name=_('Work start time'), **work_time_args)
    work_time_end = models.TimeField(verbose_name=_('Work end time'), **work_time_args)
    shift_finish_on_next_day = models.BooleanField(default=False, verbose_name=_('Shift finish on next day'))

    lunch_time_begin = models.TimeField(verbose_name=_('Lunch start time'), null=True, blank=True)
    lunch_time_end = models.TimeField(verbose_name=_('Lunch end time'), null=True, blank=True)
    appointment_duration = models.PositiveIntegerField(
        verbose_name=_('Appointment duration (seconds)'), default=3600
    )

    class Meta:
        abstract = True

    def get_work_time_borders(self):
        return self.work_time_begin, self.work_time_end


class WorkRegimeExceptions(BaseWorkRegimeDetails):
    IS_WORK_TIME_OPTIONAL = True

    date = models.DateField(verbose_name=_('Date'))
    is_holiday = models.BooleanField(default=False, verbose_name=_('Is holiday'))

    def __str__(self):
        holiday_msg = " {}".format(_("Holiday")) if self.is_holiday else ""
        return f"{self.work_regime.name} ({self.date}{holiday_msg})"

    class Meta:
        verbose_name = _('Exception of work regime')
        verbose_name_plural = _('Exceptions of work regime')
        unique_together = (("work_regime", "date"),)


class WorkRegimeDetail(BaseWorkRegimeDetails):
    day_of_week = models.SmallIntegerField(choices=DAYS_OF_THE_WEEK.items(), verbose_name=_("Day of the week"))

    def __str__(self):
        return f"{self.work_regime.name} ({DAYS_OF_THE_WEEK.get(self.day_of_week)})"

    class Meta:
        verbose_name = _('Details of work regime')
        verbose_name_plural = _('Details of work regime')
        unique_together = (("work_regime", "day_of_week"),)
