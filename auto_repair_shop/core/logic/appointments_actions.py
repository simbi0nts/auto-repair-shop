
import datetime as dt
import inspect
from dataclasses import dataclass

from django.utils.translation import gettext_lazy as _

from core.logic.appointments_info import get_available_appointments
from core.models.staff import Workman
from core.models.workflow import Appointments, AppointmentsArchive
from core.utils.dateutils import string_to_date


@dataclass
class AppointmentArgs:
    time: dt.datetime = None
    new_time: dt.datetime = None
    workman_id: int = None
    user_id: int = None

    @classmethod
    def proc_item(cls, key, val) -> dict:
        if key in ('time', 'new_time'):
            if type(val) == str:
                val = string_to_date(val)

        return val

    @classmethod
    def from_dict(cls, env: dict):
        return cls(**{
            k: cls.proc_item(k, v) for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })


class AppointmentsModelCommunicator(object):

    def __init__(self, *args, **kw):
        super().__init__()
        self.from_archive = kw.get("from_archive", False)
        self.filter_args = AppointmentArgs.from_dict(kw)

    @property
    def work_regime(self):
        return Workman.objects.get(
            id=self.filter_args.workman_id
        ).repair_shop.default_work_regime

    @property
    def work_regime_details(self):
        return self.work_regime.get_wrd(self.date)

    @property
    def date(self):
        if type(self.filter_args.time) == dt.datetime:
            return self.filter_args.time.date()

    @property
    def new_date(self):
        if type(self.filter_args.new_time) == dt.datetime:
            return self.filter_args.new_time.date()

    @property
    def duration(self):
        return self.work_regime_details.appointment_duration

    @property
    def _orm_model(self):
        return self._get_orm_model()

    def _get_orm_model(self):
        if self.from_archive:
            return AppointmentsArchive
        else:
            return Appointments

    def _get_record(self):
        record = self._orm_model.objects.filter(
            customer_id=self.filter_args.user_id,
            workman_id=self.filter_args.workman_id,
            date=self.date,
            time=self.filter_args.time,
        ).first()

        msg = _("Appointment not found") if not record else _("Success")
        return record, msg

    def _check_if_time_available(self, _time):
        is_exist = self._orm_model.objects.filter(
            workman_id=self.filter_args.workman_id,
            date=_time.date(),
            time=_time
        ).exists()

        msg = _("Chosen time is not available") if is_exist else _("Success")
        return is_exist, msg

    def _check_if_time_valid(self, _time):
        args = {
            "date": _time.date(),
            "workman_id": self.filter_args.workman_id,
        }
        appointments = get_available_appointments(**args)

        for appointment in appointments:
            if appointment.datetime_begin == _time:
                return False, _("Success")

        return True, _("Chosen time is not valid")

    def _check_time(self, _time):
        is_error, msg = self._check_if_time_available(_time)
        if is_error:
            return is_error, msg

        is_error, msg = self._check_if_time_valid(_time)
        if is_error:
            return is_error, msg

        return False, None

    def _create(self):
        self._orm_model.objects.create(
            customer_id=self.filter_args.user_id,
            workman_id=self.filter_args.workman_id,
            date=self.date,
            time=self.filter_args.time,
            work_regime=self.work_regime,
            duration=self.duration,
        )

    def create(self):
        is_error, msg = self._check_time(self.filter_args.time)
        if not is_error:
            self._create()
        return is_error, msg

    def delete(self):
        rec, msg = self._get_record()
        if rec:
            rec.delete()
            return False, msg

        return True, msg

    def _move(self, rec, new_time):
        rec.date = self.new_date
        rec.time = new_time
        rec.save()

    def move(self):
        rec, msg = self._get_record()
        if not rec:
            return True, msg

        new_time = self.filter_args.new_time

        is_error, msg = self._check_time(new_time)
        if not is_error:
            self._move(rec, new_time)
        return is_error, msg


def make_an_appointment(**args):
    return AppointmentsModelCommunicator(**args).create()


def move_an_appointment(**args):
    return AppointmentsModelCommunicator(**args).move()


def delete_an_appointment(**args):
    return AppointmentsModelCommunicator(**args).delete()
