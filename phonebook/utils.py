import os
import sys


def concat_dict_values(data: dict) -> str:
    """Concatenation of all dict values in single string."""
    return ''.join(
        str(value).replace(' ', '').lower() for value in data.values()
    )


def clear() -> None:
    """Clearing the terminal."""
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def exit() -> None:
    """Terminate the program."""
    clear()
    sys.exit()


def field_separator(sep_char: str = '-', length: int = 30) -> str:
    """Constructing field separator."""
    carry: str = '\n'
    return carry + sep_char*length + carry
