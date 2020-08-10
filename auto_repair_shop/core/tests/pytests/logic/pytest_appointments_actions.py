
from datetime import datetime

import pytest

from core.logic.appointments_actions import (delete_an_appointment,
                                             make_an_appointment,
                                             move_an_appointment)
from core.models.workflow import Appointments
from core.tests.pytests.model_fillers.structure import (
    generate_repair_shop, generate_user, generate_user_car,
    generate_work_regime, generate_work_regime_details, generate_workmans)

# from core.tests.pytests.model_fillers.data import generate_appointments, generate_appointments_daterange


class TestAppointmentsProcessors(object):
    def generate_data(self, is_range=False):
        self._datetime = datetime(2020, 8, 5, 9)
        self._datetime_end = datetime(2020, 8, 10, 18)
        self.user = generate_user()
        self.user_car = generate_user_car(self.user)
        self.repair_shop = rs = generate_repair_shop()
        self.work_regime = wr = generate_work_regime(rs)
        self.work_regime_details = generate_work_regime_details(wr)
        self.workmans = generate_workmans(rs)

        # NOTICE: IN CURRENT CASE THERE IS LUNCH BREAK AT WORK_BEGIN + 5hrs
        # missed_hours = (2, 3, 5)  # time delta in hours from work_time begin
        # if is_range:
        #     self.appointments = generate_appointments_daterange(
        #         self.workmans, self.user, self.work_regime, self._datetime, self._datetime_end, missed_hours
        #     )
        # else:
        #     self.appointments = generate_appointments(
        #         self.workmans, self.user, self.work_regime, self._datetime, missed_hours
        #     )

    @pytest.mark.django_db
    def test_create(self):
        self.generate_data()

        _date = datetime(2020, 8, 5, 12)
        data = {
            "time": _date,
            "workman_id": self.workmans[3].id,
            "user_id": self.user.id
        }

        is_err, msg = make_an_appointment(**data)

        assert is_err is False

        assert Appointments.objects.filter(
            date=_date.date(),
            time=_date,
            workman__id=self.workmans[3].id,
            customer_id=self.user.id
        ).exists()

    @pytest.mark.django_db
    def test_delete(self):
        self.generate_data(is_range=True)

        _date = datetime(2020, 8, 5, 12)
        data = {
            "time": _date,
            "workman_id": self.workmans[3].id,
            "user_id": self.user.id
        }

        is_err, msg = make_an_appointment(**data)

        assert is_err is False

        assert Appointments.objects.filter(
            date=_date.date(),
            time=_date,
            workman__id=self.workmans[3].id,
            customer_id=self.user.id
        ).exists()

        is_err, msg = delete_an_appointment(**data)

        assert is_err is False

        assert not Appointments.objects.filter(
            date=_date.date(),
            time=_date,
            workman__id=self.workmans[3].id,
            customer_id=self.user.id
        ).exists()

    @pytest.mark.django_db
    def test_move(self):
        self.generate_data()

        _date = datetime(2020, 8, 5, 12)
        new_date = datetime(2020, 8, 5, 15)

        data = {
            "time": _date,
            "workman_id": self.workmans[3].id,
            "user_id": self.user.id
        }

        is_err, msg = make_an_appointment(**data)

        assert is_err is False

        assert Appointments.objects.filter(
            date=_date.date(),
            time=_date,
            workman__id=self.workmans[3].id,
            customer_id=self.user.id
        ).exists()

        assert not Appointments.objects.filter(
            date=new_date.date(),
            time=new_date,
            workman__id=self.workmans[3].id,
            customer_id=self.user.id
        ).exists()

        data.update({
            "new_time": new_date
        })

        is_err, msg = move_an_appointment(**data)

        assert is_err is False

        assert not Appointments.objects.filter(
            date=_date.date(),
            time=_date,
            workman__id=self.workmans[3].id,
            customer_id=self.user.id
        ).exists()

        assert Appointments.objects.filter(
            date=new_date.date(),
            time=new_date,
            workman__id=self.workmans[3].id,
            customer_id=self.user.id
        ).exists()
