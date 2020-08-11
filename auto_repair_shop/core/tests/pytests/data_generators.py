
from datetime import datetime

import pytz
from django.utils.timezone import make_aware

from core.tests.pytests.model_fillers.data import (
    generate_appointments, generate_appointments_daterange)
from core.tests.pytests.model_fillers.structure import (
    generate_repair_shop, generate_user, generate_user_car,
    generate_work_regime, generate_work_regime_details, generate_workmans)


class SimpleTestDataGenerator(object):

    def generate_data(self, is_range=False):
        self._datetime = make_aware(datetime(2020, 8, 5, 9), pytz.UTC)
        self._datetime_end = make_aware(datetime(2020, 8, 10, 15), pytz.UTC)
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
