
from django.utils.timezone import get_current_timezone
from django.utils.translation import gettext_lazy as _

from core.logic.appointments_actions import make_an_appointment
from core.logic.appointments_info import (get_all_appointments,
                                          get_occupied_appointments,
                                          get_available_appointments)
from core.logic.custom_exceptions import MethodNotFound, ProcessorNotFound
from core.utils.message_formers import form_error
from core.utils.parser import parse_get, parse_post, parse_datetime


class BaseContextProcessor(object):

    @staticmethod
    def get_timezone(data):
        return data.get("timezone", get_current_timezone())

    @classmethod
    def process(cls, request, *args, **kwargs):
        handler_method_name = 'process_{}'.format(request.method)
        handler = getattr(cls, handler_method_name.lower(),
                          cls.http_method_not_found)
        return handler(request, *args, **kwargs)

    @classmethod
    def http_method_not_found(cls, request, *args, **kwargs):
        raise MethodNotFound(request.method)


class MakeAppointmentLogic(BaseContextProcessor):

    @classmethod
    def process_post(cls, request):
        data = parse_post(request)

        timezone = cls.get_timezone(data)
        data = parse_datetime(data, timezone=timezone)

        data.update({
            'user_id': request.user.id
        })
        is_error, error_msg = make_an_appointment(**data)
        return {
            "is_error": is_error,
            "info": error_msg
        }


class CheckRepairShopWorkloadLogic(BaseContextProcessor):

    @classmethod
    def process_get(cls, request):
        data = parse_get(request)

        timezone = cls.get_timezone(data)
        data = parse_datetime(data, timezone=timezone)

        workload = cls.get_workload(data)
        return workload

    @classmethod
    def get_workload(cls, data: dict) -> dict:

        def _perc(v1: float, v2: float):
            return round(v1 / v2 * 100, 2) if v2 else None

        try:
            all_appointments = get_all_appointments(**data)
            occupied_appointments = get_occupied_appointments(**data)
        except ProcessorNotFound:
            return form_error(_("Wrong arguments"))

        all_appointments_cnt = len(all_appointments)
        occupied_appointments_cnt = len(occupied_appointments)

        if all_appointments_cnt == 0:
            return form_error(_("No appointments available for chosen date"))

        perc = _perc(occupied_appointments_cnt, all_appointments_cnt)

        msg = _("Current workload")
        workload = f"{msg}: {perc}%"

        return {
            "is_error": False,
            "info": workload
        }


class GetAvailableAppointmentTimeLogic(BaseContextProcessor):

    @classmethod
    def process_get(cls, request):
        data = parse_get(request)

        timezone = cls.get_timezone(data)
        data = parse_datetime(data, timezone=timezone)

        result = cls.get_available_time(data)
        return result

    @classmethod
    def get_available_time(cls, data: dict) -> dict:
        available_time = []

        try:
            available_appointments = get_available_appointments(**data)
        except ProcessorNotFound:
            return form_error(_("Wrong arguments"))

        date_format = '%Y/%m/%d %H:%M'
        timezone = cls.get_timezone(data)

        for appointment in available_appointments:
            available_time.append(appointment.datetime_begin)

        appointments = sorted(set(available_time))
        appointments = [apt.astimezone(timezone).strftime(date_format) for apt in appointments]

        msg = _("Available time")
        workload = f"{msg}: {'; '.join(appointments)}"

        return {
            "is_error": False,
            "info": workload
        }
