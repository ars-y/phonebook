import re

from .ioworkers import console


def _validate_phone_number(value: str) -> str:
    """Validate phone number."""
    pattern = r'^([+]?[\s0-9]+)?(\d{3}|[(]?[0-9]+[)])?([-]?[\s]?[0-9])+$'
    if value and not re.search(pattern, value):
        raise ValueError('[Err] Invalid phone number')

    return value


def validate_field(value: str) -> str:
    """Validate Contact field value."""
    while True:
        if not value:
            return value

        try:
            return _validate_phone_number(value)

        except ValueError as exc:
            console.write(exc)
            value = console.read('Enter value: ')
