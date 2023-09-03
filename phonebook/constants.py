import colorama
from pathlib import Path

from .models import TOTAL_FIELDS


BASE_DIR: Path = Path(__file__).resolve().parent.parent

CONTACTS_DIR: Path = BASE_DIR / 'files'

CONTACTS_FILE: Path = CONTACTS_DIR / 'contacts.csv'

DB_DIR: Path = BASE_DIR / 'data'

DB_PATH: str = str(DB_DIR / 'contacts.db')

FILE_INIT_KEY: str = '--init'

UPLOAD_FILE_KEY: str = '--upload'

PAGE_SIZE: int = 6

FRAME_DESIGN: str = '#'

FRAME_SIZE: int = 80

FIRST, *_, LAST = range(PAGE_SIZE)

FIRST_FIELD, *_, LAST_FIELD = range(1, TOTAL_FIELDS + 1)


class Button:
    """Availible key buttons."""

    ADD: str = 'a'
    CANCEL: str = 'c'
    DELETE: str = 'd'
    EDIT: str = 'e'
    FIND: str = 'f'
    HELP: str = 'h'
    HELP_L: str = 'help'
    NEXT: str = 'n'
    PREV: str = 'p'
    QUIT: str = 'q'
    SAVE: str = 's'


class ReportState:
    """Operation report state."""

    DECLINE: str = ''.join(
        (
            colorama.Fore.RED,
            'CHANGES DECLINED',
            colorama.Fore.RESET,
        )
    )
    ACCEPT: str = ''.join(
        (
            colorama.Fore.GREEN,
            'CHANGES ACCEPTED',
            colorama.Fore.RESET,
        )
    )
    DONOTHING: str = ''.join(
        (
            colorama.Fore.YELLOW,
            'NO CHANGES APPLIED',
            colorama.Fore.RESET,
        )
    )
