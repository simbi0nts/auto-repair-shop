
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

        total_appointments_cnt = 5 * 8
        occupied_appointments_cnt = len(self.appointments)

        assert len(res1) == total_appointments_cnt
        assert len(res2) == total_appointments_cnt - occupied_appointments_cnt
        assert len(res3) == occupied_appointments_cnt

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

        total_appointments_cnt = 30 * 8
        occupied_appointments_cnt = len(self.appointments)

        assert len(res1) == total_appointments_cnt
        assert len(res2) == total_appointments_cnt - occupied_appointments_cnt
        assert len(res3) == occupied_appointments_cnt

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

        total_appointments_cnt = 5 * 8
        occupied_appointments_cnt = len(self.appointments)

        assert len(res1) == total_appointments_cnt
        assert len(res2) == total_appointments_cnt - occupied_appointments_cnt
        assert len(res3) == occupied_appointments_cnt

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

        total_appointments_cnt = 30 * 8
        occupied_appointments_cnt = len(self.appointments)

        assert len(res1) == total_appointments_cnt
        assert len(res2) == total_appointments_cnt - occupied_appointments_cnt
        assert len(res3) == occupied_appointments_cnt

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
        assert len(res2) == 2
        assert len(res3) == 6

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

        assert len(res1) == 8 * 6
        assert len(res2) == 2 * 6
        assert len(res3) == 6 * 6
