
from collections.abc import Iterable
from typing import Union

from core.utils.dateutils import string_to_date


def _parse_request(request, method: str, fields: Union[str, Iterable]) -> dict:
    if not hasattr(request, method):
        return {}

    request_data = getattr(request, method)

    if fields == "__all__":
        return {k: v for k, v in request_data.items()}

    data = {}
    if isinstance(fields, Iterable):
        for field in fields:
            data[field] = request_data.get(field)

    return data


def parse_datetime(data, timezone=None):
    for k, v in data.items():
        try:
            data[k] = string_to_date(v, timezone=timezone)
        except ValueError:
            pass
    return data


def parse_get(request, fields="__all__"):
    return _parse_request(request, "GET", fields)


def parse_post(request, fields="__all__"):
    return _parse_request(request, "data", fields)
