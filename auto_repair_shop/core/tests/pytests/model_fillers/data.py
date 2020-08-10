

from datetime import datetime, timedelta

from core.models import Appointments  # , AppointmentsArchive


def generate_user():
    from core.tests.pytests.model_fillers.data import generate_user as generate_user_
    return generate_user_()


def generate_work_regime():
    from core.tests.pytests.model_fillers.data import generate_work_regime as generate_work_regime_
    return generate_work_regime_()


def generate_workmans(rs):
    from core.tests.pytests.model_fillers.data import generate_workmans as generate_workmans_
    return generate_workmans_(rs)


def generate_appointments(workmans=None, customer=None, work_regime=None,
                          _datetime=datetime(2020, 8, 5, 9), missed_hours=(2, 3, 5)):

    if customer is None:
        customer = generate_user()

    if work_regime is None:
        work_regime = generate_work_regime()

    if workmans is None:
        workmans = generate_workmans(work_regime.repair_shop)

    _date = _datetime.date()

    appointments = []

    for w_id in range(3):
        for hour_delta in range(8):
            if missed_hours and hour_delta in missed_hours:
                continue  # emulate empty slots

            appointments.append(
                Appointments.objects.create(
                    date=_date,
                    time=_datetime + timedelta(hours=hour_delta),
                    duration=3600,
                    workman=workmans[w_id],
                    customer=customer,
                    work_regime=work_regime,
                )
            )

    return appointments


def generate_appointments_daterange(workmans=None, customer=None, work_regime=None,
                                    dt_begin=datetime(2020, 8, 5, 9),
                                    dt_emd=datetime(2020, 8, 10, 18),
                                    missed_hours=(2, 3, 5)):

    if customer is None:
        customer = generate_user()

    if work_regime is None:
        work_regime = generate_work_regime()

    if workmans is None:
        workmans = generate_workmans(work_regime.repair_shop)

    appointments = []
    _datetime = dt_begin
    while dt_emd > _datetime:
        appointments += generate_appointments(workmans, customer, work_regime, _datetime, missed_hours)
        _datetime += timedelta(days=1)

    return appointments


def generate_appointments_archive():
    pass  # TODO
