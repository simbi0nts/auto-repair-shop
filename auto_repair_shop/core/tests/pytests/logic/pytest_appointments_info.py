
from datetime import datetime

import pytest

from core.logic.appointments_info import (get_all_appointments,
                                          get_available_appointments,
                                          get_occupied_appointments)
from core.tests.pytests.model_fillers.data import (
    generate_appointments, generate_appointments_daterange)
from core.tests.pytests.model_fillers.structure import (
    generate_repair_shop, generate_user, generate_user_car,
    generate_work_regime, generate_work_regime_details, generate_workmans)


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
        missed_hours = (2, 3, 5)  # time delta in hours from work_time begin
        if is_range:
            self.appointments = generate_appointments_daterange(
                self.workmans, self.user, self.work_regime, self._datetime, self._datetime_end, missed_hours
            )
        else:
            self.appointments = generate_appointments(
                self.workmans, self.user, self.work_regime, self._datetime, missed_hours
            )

    @pytest.mark.django_db
    def test_workload_DateProcessor(self):
        self.generate_data()

        data = {
            "date": self._datetime,
        }

        res1 = get_all_appointments(**data)
        res2 = get_available_appointments(**data)
        res3 = get_occupied_appointments(**data)

        assert len(res1) == 40
        assert len(res2) == 25
        assert len(res3) == 15

    @pytest.mark.django_db
    def test_workload_DateRangeProcessor(self):
        self.generate_data(is_range=True)

        data = {
            "datetime_begin": self._datetime,
            "datetime_end": self._datetime_end,
        }

        res1 = get_all_appointments(**data)
        res2 = get_available_appointments(**data)
        res3 = get_occupied_appointments(**data)

        assert len(res1) == 240
        assert len(res2) == 150
        assert len(res3) == 90

    @pytest.mark.django_db
    def test_workload_DateShopProcessor(self):
        self.generate_data()

        data = {
            "date": self._datetime,
            "repair_shop_id": self.repair_shop.id
        }

        res1 = get_all_appointments(**data)
        res2 = get_available_appointments(**data)
        res3 = get_occupied_appointments(**data)

        assert len(res1) == 40
        assert len(res2) == 25
        assert len(res3) == 15

    @pytest.mark.django_db
    def test_workload_DateRangeShopProcessor(self):
        self.generate_data(is_range=True)

        data = {
            "datetime_begin": self._datetime,
            "datetime_end": self._datetime_end,
            "repair_shop_id": self.repair_shop.id
        }

        res1 = get_all_appointments(**data)
        res2 = get_available_appointments(**data)
        res3 = get_occupied_appointments(**data)

        assert len(res1) == 240
        assert len(res2) == 150
        assert len(res3) == 90

    @pytest.mark.django_db
    def test_workload_DateWorkmanProcessor(self):
        self.generate_data(is_range=True)

        data = {
            "date": self._datetime,
            "workman_id": self.workmans[0].id
        }

        res1 = get_all_appointments(**data)
        res2 = get_available_appointments(**data)
        res3 = get_occupied_appointments(**data)

        assert len(res1) == 8
        assert len(res2) == 3
        assert len(res3) == 5

    @pytest.mark.django_db
    def test_workload_DateRangeWorkmanProcessor(self):
        self.generate_data(is_range=True)

        data = {
            "datetime_begin": self._datetime,
            "datetime_end": self._datetime_end,
            "workman_id": self.workmans[0].id
        }

        res1 = get_all_appointments(**data)
        res2 = get_available_appointments(**data)
        res3 = get_occupied_appointments(**data)

        assert len(res1) == 48
        assert len(res2) == 18
        assert len(res3) == 30
