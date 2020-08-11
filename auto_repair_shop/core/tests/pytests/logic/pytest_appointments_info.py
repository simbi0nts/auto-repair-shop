
import pytest

from core.logic.appointments_info import (get_all_appointments,
                                          get_available_appointments,
                                          get_occupied_appointments)
from core.tests.pytests.data_generators import SimpleTestDataGenerator


class TestAppointmentsProcessors(SimpleTestDataGenerator):

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
