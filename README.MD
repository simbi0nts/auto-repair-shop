

## **1) Install**

1.a) Via Docker

    git clone https://github.com/simbi0nts/auto-repair-shop.git
    cd auto-repair-shop
    docker-compose up -d

*Note: other services might be blocking 80 port. Either change it in docker settings or stop these services.*

For example, to disable nginx:

    sudo nginx -s stop

1.b) Old-school

    git clone https://github.com/simbi0nts/auto-repair-shop.git
    cd auto-repair-shop
    pip install -r requirements.txt
    pip cd auto_repair_shop
    python manage.py runserver 0.0.0.0:80

*Note 1: Be sure to set DEBUG, SECRET_KEY and DJANGO_ALLOWED_HOSTS env variables*

*Note 2: I'm highly recommend to use virtual environment*

2 ) Web now should be serving at http:\\localhost

## **2) Usage**

**2.1) Get JWT token:**

    host:port/api/token/

args to send: 

    login
    password

args to return

    refresh (token to refresh access token)
    access (token to access API)


**2.2) Refresh JWT token**

    host:port/api/token/refresh/

args to send: 

    refresh (token to refresh access token)

args to return

    access (token to access API)


*Note: Next api methods allowed only when access token (from 2.1 and 2.2) provided:*

    headers:
        Authorization: {access token}
        (ex. "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTk2OTA2MzAzLCJqdGkiOiJlMTY1N2NmMTNkZTY0ODIxYTMxYmY5MTg0NjIwODc0OCIsInVzZXJfaWQiOjF9.GlhsYjQ6hn-rPCEXaKXcBH1DxZyMpEq3zTEpLZAzZPE")


**2.3) Make an appointment**

    host:port/api/make_appointment/

args to send: 

    time (type: str)  # ex. "2020-01-01 09:00"
    workman_id
    timezone (type: str) (optional)  # ex. "Europe/Moscow" (default)

args to return

    is_error
    info

**2.4)Get an available appointment time**

    host:port/api/get_available_appointment_time/

args to send: 

    date (type: str)  # ex. "2020-01-01"
    repair_shop_id (optional)
    workman_id (optional)
    timezone (type: str) (optional)  # ex. "Europe/Moscow" (default)

OR

    datetime_begin (type: str)  # ex. "2020-01-01 09:00"
    datetime_end (type: str)  # ex. "2020-01-01 18:00"
    repair_shop_id (optional)
    workman_id (optional)
    timezone (type: str) (optional)  # ex. "Europe/Moscow" (default)

*Note: datetime_begin <= assumed appointment time < datetime_end*

args to return

    is_error
    info  # ex. 'Available time: : 2020/08/05 14:00; 2020/08/05 15:00; 2020/08/05 20:00'

**2.5) Check workshop workload**

    host:port/api/check_workload/

args to send: 

    date (type: str)  # ex. "2020-01-01"
    repair_shop_id (optional)
    workman_id (optional)
    timezone (type: str) (optional)  # ex. "Europe/Moscow" (default)

   OR

    datetime_begin (type: str)  # ex. "2020-01-01 09:00"
    datetime_end (type: str)  # ex. "2020-01-01 18:00"
    repair_shop_id (optional)
    workman_id (optional)
    timezone (type: str) (optional)  # ex. "Europe/Moscow" (default)

*Note: datetime_begin <= assumed appointment time < datetime_end*

args to return

    is_error
    info  # ex. 'Current workload: 62.5%'


## **3) Tests**

a) Via Docker

    docker-compose exec -T web pytest

b) Old-school

    pytest -v -c auto_repair_shop/pytest.ini


## **4) Possible improvements**

1) User timezone to set up in profile
2) User language to set up in profile
3) Web representation of API functionality


## **9) Additional Info**

Language and timezone can be set in settings.py.

Current project provided with sqlite db with some custom data. 

Admin credentials: admin/admin

Supported datetime formats:

    '%Y-%m-%d %H:%M:%S.%f'
    '%Y-%m-%dT%H:%M:%S.%f'
    '%d.%m.%Y %H:%M:%S'
    '%Y-%m-%dT%H:%M:%S'
    '%Y-%m-%d %H:%M:%S'
    '%d.%m.%Y %H:%M'
    '%Y-%m-%d %H:%M'
    '%d.%m.%Y'
    '%Y-%m-%d'
    '%Y-%m'

User Timezone info could be provided with

    Intl.DateTimeFormat().resolvedOptions().timeZone

(on client)
