import re
from .ioworkers import console


def validate_field(name: str, value: str) -> str:
    pattern = r'^(\+)[1-9][0-9\-\(\)\.]{9,15}$'
    if value and not re.search(pattern, value):
        raise ValueError(f'invalid value `{value}` for field `{name}`')
    return value


def validate(name: str, value: str) -> str:
    while True:

        try:
            value = validate_field(name, value)
            break

        except ValueError as exc:
            print(exc)
            value = console.read('Enter value: ')

    return value
