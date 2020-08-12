
import datetime as dt
import inspect
from dataclasses import asdict, dataclass
from typing import List

from django.db.models import Q, QuerySet
from django.utils.timezone import make_aware, get_current_timezone

from core.logic.custom_exceptions import ProcessorNotFound, WrongArgumentsHasBeenPassed
from core.models.repair_shop import RepairShop
from core.models.staff import Workman
from core.models.work_regime import WorkRegime
from core.models.workflow import Appointments, AppointmentsArchive
from core.utils.dateutils import string_to_date


@dataclass
class AppointmentInfo:
    repair_shop_id: int
    workman_id: int
    datetime_begin: dt.datetime
    datetime_end: dt.datetime
    duration: int
    is_occupied: bool


# Very base classes

class BaseDataProcessor(object):

    def __init__(self, *args, **kw):
        super().__init__()
        self.from_archive = kw.get("from_archive", False)
        self.filter_args = kw

    @property
    def _orm_model(self):
        return self._get_orm_model()

    def _get_orm_model(self):
        if self.from_archive:
            return AppointmentsArchive
        else:
            return Appointments

    def get_qs(self) -> QuerySet:
        return self._orm_model.objects.all()

    def filter_qs(self, qs: QuerySet):
        raise NotImplementedError

    def process_qs(self, qs: QuerySet):
        raise NotImplementedError

    def collect_appointments(self) -> List[AppointmentInfo]:
        qs = self.get_qs()
        qs = self.filter_qs(qs)
        appointments = self.process_qs(qs)
        return appointments

    def _process_workman_day(self, qs: QuerySet, _date: dt.date,
                             wrd: QuerySet, workman: QuerySet,
                             wt_begin: dt.datetime = None,
                             wt_end: dt.datetime = None, **kwargs) -> List[AppointmentInfo]:

        def _comb(v1: dt.date, v2: dt.time) -> dt.datetime:
            return make_aware(dt.datetime.combine(v1, v2), get_current_timezone())

        def is_lunchtime(lt_begin: dt.datetime, lt_end: dt.datetime, cur_time: dt.datetime) -> bool:
            if any(val is None for val in (lt_begin, lt_end, cur_time)):
                return False
            else:
                return lt_begin <= cur_time and cur_time < lt_end

        res = []

        repair_shop_id = workman.repair_shop.id
        appointment_dur = wrd.appointment_duration

        work_time_begin = _comb(_date, wrd.work_time_begin)
        work_time_end = _comb(_date, wrd.work_time_end)

        if wt_begin:
            work_time_begin = max(wt_begin, work_time_begin)

        if wt_end:
            work_time_end = min(wt_end, work_time_end)

        lunch_time_begin = None
        if wrd.lunch_time_begin:
            lunch_time_begin = _comb(_date, wrd.lunch_time_begin)

        lunch_time_end = None
        if wrd.lunch_time_end:
            lunch_time_end = _comb(_date, wrd.lunch_time_end)

        if wrd.shift_finish_on_next_day:
            work_time_end += dt.timedelta(days=1)

        _current_time_begin = work_time_begin

        while _current_time_begin < work_time_end:
            _current_time_end = _current_time_begin + dt.timedelta(seconds=appointment_dur)

            if is_lunchtime(lunch_time_begin, lunch_time_end, _current_time_begin):
                _current_time_begin = _current_time_end
                continue

            appointment = qs.filter(
                time=_current_time_begin,
                workman=workman
            ).first()

            is_occupied = bool(appointment)

            res.append(
                AppointmentInfo(
                    repair_shop_id,
                    workman.id,
                    _current_time_begin,
                    _current_time_end,
                    appointment_dur,
                    is_occupied
                )
            )

            _current_time_begin = _current_time_end

        return res


class BaseDateProcessor(BaseDataProcessor):

    @property
    def date(self):
        return self.filter_args["date"]

    @property
    def date_qs(self):
        return {
            "date": self.date,
        }

    def _process_day(self, qs: QuerySet, work_regime: QuerySet, **kwargs) -> List[AppointmentInfo]:
        res = []

        _date = kwargs.get("date", self.date)

        wrd = work_regime.get_wrd(_date)
        if not wrd:
            return res

        repair_shop = wrd.work_regime.repair_shop

        workman_ids = kwargs.get('workman_ids')
        if workman_ids:
            workman_qs = Workman.objects.filter(id__in=workman_ids)
        else:
            workman_qs = Workman.objects.filter(
                Q(repair_shop__default_work_regime=wrd.work_regime) | Q(individual_work_regime=wrd.work_regime),
                repair_shop=repair_shop,
            )

        for workman in workman_qs:
            res += self._process_workman_day(qs, _date, wrd, workman, **kwargs)

        return res

    def _process(self, *args, **kwargs):
        return self._process_day(*args, **kwargs)


class BaseDateRangeProcessor(BaseDateProcessor):

    @property
    def datetime_begin(self):
        return self.filter_args["datetime_begin"]

    @property
    def datetime_end(self):
        return self.filter_args["datetime_end"]

    @property
    def date_qs(self):
        return {
            "date__gte": self.datetime_begin.date(),
            "date__lte": self.datetime_end.date(),
        }

    def _process_date_range(self, qs: QuerySet, work_regime: QuerySet, **kwargs) -> List[AppointmentInfo]:
        res = []
        kwargs['wt_begin'] = self.datetime_begin
        kwargs['wt_end'] = self.datetime_end

        start_date = self.datetime_begin.date()
        end_date = self.datetime_end.date()
        day_count = (end_date - start_date).days + 1

        for _date in (start_date + dt.timedelta(n) for n in range(day_count)):
            res += self._process_day(qs, work_regime, date=_date, **kwargs)

        return res

    def _process(self, *args, **kwargs):
        return self._process_date_range(*args, **kwargs)


# No workman, no shop

class SimpleDateProcessor:
    def filter_qs(self, qs: QuerySet) -> QuerySet:
        return qs.filter(
            **self.date_qs
        )

    def process_qs(self, qs: QuerySet) -> List[AppointmentInfo]:
        res = []
        for work_regime in WorkRegime.objects.all():
            res += self._process(qs, work_regime)

        return res


class DateProcessor(SimpleDateProcessor, BaseDateProcessor):
    pass


class DateRangeProcessor(SimpleDateProcessor, BaseDateRangeProcessor):
    pass


# Shop

class ShopProcessor:
    @property
    def work_regime(self):
        return RepairShop.objects.get(
            id=self.filter_args["repair_shop_id"]
        ).default_work_regime

    def filter_qs(self, qs: QuerySet) -> QuerySet:
        return qs.filter(
            workman__repair_shop_id=self.filter_args["repair_shop_id"],
            work_regime=self.work_regime,
            **self.date_qs
        )

    def process_qs(self, qs: QuerySet) -> List[AppointmentInfo]:
        workman_ids = [
            w.id for w in Workman.objects.filter(repair_shop_id=self.filter_args["repair_shop_id"])
        ]
        res = self._process(qs, self.work_regime, workman_ids=workman_ids)
        return res


class DateShopProcessor(ShopProcessor, BaseDateProcessor):
    pass


class DateRangeShopProcessor(ShopProcessor, BaseDateRangeProcessor):
    pass


# Workman

class WorkmanProcessor:
    @property
    def work_regime(self):
        workmam = Workman.objects.get(id=self.filter_args["workman_id"])
        return workmam.individual_work_regime or workmam.repair_shop.default_work_regime

    def filter_qs(self, qs: QuerySet) -> QuerySet:
        return qs.filter(
            workman_id=self.filter_args["workman_id"],
            work_regime=self.work_regime,
            **self.date_qs
        )

    def process_qs(self, qs: QuerySet) -> List[AppointmentInfo]:
        workman_ids = [self.filter_args["workman_id"]]
        res = self._process(qs, self.work_regime, workman_ids=workman_ids)
        return res


class DateWorkmanProcessor(WorkmanProcessor, BaseDateProcessor):
    pass


class DateRangeWorkmanProcessor(WorkmanProcessor, BaseDateRangeProcessor):
    pass


@dataclass
class ProcessorArgs:
    date: dt.date = None
    datetime_begin: dt.datetime = None
    datetime_end: dt.datetime = None
    repair_shop_id: int = None
    workman_id: int = None
    from_archive: bool = False

    @classmethod
    def proc_item(cls, key, val) -> dict:
        if key == 'date':
            if type(val) == str:
                val = string_to_date(val)
            if type(val) == dt.datetime:
                val = val.date()

        if key in ('datetime_begin', 'datetime_end'):
            if type(val) == str:
                val = string_to_date(val)

        if key in ('repair_shop_id', 'workman_id'):
            if type(val) == str:
                val = int(val)

        return val

    @classmethod
    def from_dict(cls, env: dict):
        return cls(**{
            k: cls.proc_item(k, v) for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })

    @property
    def processor(self):
        if self.date is not None:
            if self.workman_id is not None:
                return DateWorkmanProcessor

            if self.repair_shop_id is not None:
                return DateShopProcessor

            return DateProcessor

        if self.datetime_begin is not None and self.datetime_end is not None:
            if self.workman_id is not None:
                return DateRangeWorkmanProcessor

            if self.repair_shop_id is not None:
                return DateRangeShopProcessor

            return DateRangeProcessor

        raise ProcessorNotFound

    def get_processor(self):
        return self.processor(**asdict(self))


def get_data_processor__old(kw):
    # Deprecated

    def filter_kw(kw):
        valid_args = ("date", "datetime_begin", "datetime_end", "repair_shop_id", "workman_id")
        return {key: val for key, val in kw.items() if key in valid_args}

    kw_to_compare = filter_kw(kw)

    kw_processor_relation = {
        ("date", ): DateProcessor,
        ("datetime_begin", "datetime_end", ): DateRangeProcessor,
        ("date", "repair_shop_id", ): DateShopProcessor,
        ("datetime_begin", "datetime_end", "repair_shop_id", ): DateRangeShopProcessor,
        ("date", "workman_id", ): DateWorkmanProcessor,
        ("datetime_begin", "datetime_end", "workman_id", ): DateRangeWorkmanProcessor,
    }

    kw_args = tuple(k for k in kw_to_compare)
    for k_args, processor in kw_processor_relation.items():
        if all(kw_arg in k_args for kw_arg in kw_args):
            return processor(**kw)

    raise WrongArgumentsHasBeenPassed


class AppointmentTotalInfo(object):

    def __init__(self, *args, **kw):
        """
            data processor depends on passed args:
            "date":                                                 DateProcessor (Not implemented)
            "datetime_begin" and "datetime_end":                    DateRangeProcessor (Not implemented)
            "date" and "repair_shop_id":                            DateShopProcessor
            "datetime_begin", "datetime_end" and "repair_shop_id":  DateRangeShopProcessor (Not implemented)
            "date" and "workman_id":                                DateWorkmanProcessor (Not implemented)
            "datetime_begin", "datetime_end" and "workman_id":      DateRangeWorkmanProcessor (Not implemented)
        """

        super().__init__()
        proc_dataclass = ProcessorArgs.from_dict(kw)
        self.data_processor = proc_dataclass.get_processor()
        self.appointments = []
        self.collect_data()

    def collect_data(self):
        self.appointments = self.data_processor.collect_appointments()

    def get_all_appointments(self):
        return self.appointments

    def get_available_appointments(self):
        return [apnt for apnt in self.appointments if not apnt.is_occupied]

    def get_occupied_appointments(self):
        return [apnt for apnt in self.appointments if apnt.is_occupied]


def get_all_appointments(**args):
    return AppointmentTotalInfo(**args).get_all_appointments()


def get_available_appointments(**args):
    return AppointmentTotalInfo(**args).get_available_appointments()


def get_occupied_appointments(**args):
    return AppointmentTotalInfo(**args).get_occupied_appointments()
