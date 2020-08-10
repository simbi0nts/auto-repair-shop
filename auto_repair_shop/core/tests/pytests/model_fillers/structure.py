
import datetime

from core.models import (RepairShop, User, UserCar, Workman, WorkRegime,
                         WorkRegimeDetail)


def generate_repair_shop(default_wr=None):
    repair_shop = RepairShop.objects.create(name='test-name-repair-shop')

    if default_wr is not None:
        repair_shop.default_work_regime = default_wr
        repair_shop.save()

    return repair_shop


def generate_workmans(repair_shop=None):
    if repair_shop is None:
        repair_shop = generate_repair_shop()

    workmans = []
    for suff in range(1, 6):
        workmans.append(
            Workman.objects.create(
                repair_shop=repair_shop,
                first_name=f'test-first-name-{suff}',
                middle_name=f'test-middle-name-{suff}',
                last_name=f'test-last-name-{suff}',
            )
        )

    return workmans


def generate_work_regime_exceptions(wr=None):
    pass  # TODO


def generate_work_regime_details(wr=None, with_lunch=True):
    if wr is None:
        wr = generate_work_regime()

    wrd = []
    for day_of_week in range(7):
        wrd.append(
            WorkRegimeDetail.objects.create(
                day_of_week=day_of_week,
                work_regime=wr,
                work_time_begin=datetime.time(hour=9),
                work_time_end=datetime.time(hour=18),
                lunch_time_begin=datetime.time(hour=14) if with_lunch else None,
                lunch_time_end=datetime.time(hour=15) if with_lunch else None,
                appointment_duration=3600,
                shift_finish_on_next_day=False,
            )
        )

    return wrd


def generate_work_regime(repair_shop=None):
    if repair_shop is None:
        repair_shop = generate_repair_shop()

    wr = WorkRegime.objects.create(
        name='test-name-work-regime',
        repair_shop=repair_shop,
    )

    if repair_shop.default_work_regime is None:
        repair_shop.default_work_regime = wr
        repair_shop.save()

    return wr


def generate_user():
    user = User.objects.create(
        username="Test",
        password="Test",
        is_superuser=False
    )
    return user


def generate_user_car(user=None):
    if user is None:
        user = generate_user()

    user_car = UserCar.objects.create(
        owner=user,
        model="Test-car",
        plate_num="123-test"
    )
    return user_car
