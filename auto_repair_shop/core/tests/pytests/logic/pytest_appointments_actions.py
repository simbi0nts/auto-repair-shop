
from datetime import datetime

import pytest
import pytz
from django.utils.timezone import make_aware

from core.logic.appointments_actions import (delete_an_appointment,
                                             make_an_appointment,
                                             move_an_appointment)
from core.models.workflow import Appointments
from core.tests.pytests.data_generators import SimpleTestDataGenerator


class TestAppointmentsProcessors(SimpleTestDataGenerator):

    @pytest.mark.django_db
    def test_create(self):
        self.generate_data()

        _date = datetime(2020, 8, 5, 14)
        _date = make_aware(_date, pytz.timezone("Europe/Moscow"))

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

        _date = datetime(2020, 8, 5, 14)
        _date = make_aware(_date, pytz.timezone("Europe/Moscow"))

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

        _date = datetime(2020, 8, 5, 14)
        _date = make_aware(_date, pytz.timezone("Europe/Moscow"))

        new_date = datetime(2020, 8, 5, 18)
        new_date = make_aware(new_date, pytz.timezone("Europe/Moscow"))

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
