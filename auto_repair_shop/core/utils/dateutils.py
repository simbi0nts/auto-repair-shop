
from collections.abc import Iterable
from datetime import datetime
from typing import Union

import pytz
from django.utils.timezone import make_aware, utc
from django.utils.translation import gettext_lazy as _


def string_to_date(date_string: str,
                   formats: Union[str, Iterable] = None,
                   timezone=None, naive: bool = False) -> datetime:
    if not formats:
        formats = [
            '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S.%f',
            '%d.%m.%Y %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S',
            '%d.%m.%Y %H:%M', '%Y-%m-%d %H:%M',
            '%d.%m.%Y', '%Y-%m-%d',
            '%Y-%m'
        ]
    elif isinstance(formats, str):
        formats = [formats]

    if timezone is None:
        timezone = utc
    elif isinstance(timezone, str):
        timezone = pytz.timezone(timezone)

    for mask in formats:
        try:
            _date = datetime.strptime(date_string, mask)

            return _date if naive else make_aware(_date, timezone)
        except ValueError:
            pass

    msg = _("time data '{ds}' did not match any format {f}").format(ds=date_string, f=repr(formats))
    raise ValueError(msg)
