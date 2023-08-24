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

FRAME_SIZE: int = 80


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


FIRST, *_, LAST = range(PAGE_SIZE)

field_no_first, *_, field_no_last = range(TOTAL_FIELDS)


class FrameLabel:
    """Labels for frames."""

    MAIN_HEADER: str = 'Contacts'
    MAIN_FOOTER: tuple = (
        f'[{Button.PREV}] prev',
        f'[{Button.NEXT}] next',
        f'[{FIRST}-{LAST}] select',
        f'[{Button.ADD}] add',
        f'[{Button.FIND}] find',
        f'[{Button.QUIT}] quit',
    )
    FIND_HEADER: str = 'Search'
    FIND_FOOTER: tuple = (
        f'[{Button.PREV}] prev',
        f'[{Button.NEXT}] next',
        f'[{FIRST}-{LAST}] select',
        f'[{Button.FIND}] find',
        f'[{Button.CANCEL}] cancel',
        f'[{Button.QUIT}] quit',
    )
    CREATE_HEADER: str = 'New Contact'
    CREATE_FOOTER: tuple = (
        f'[{field_no_first}-{field_no_last}] select',
        f'[{Button.SAVE}] save',
        f'[{Button.CANCEL}] cancel',
    )
    EDIT_HEADER: str = 'Edit Contact'
    EDIT_FOOTER: tuple = (
        f'[{field_no_first}-{field_no_last}] select',
        f'[{Button.SAVE}] save',
        f'[{Button.DELETE}] delete',
        f'[{Button.CANCEL}] cancel',
    )
    DETAIL_HEADER: str = 'Contact detail'
    DETAIL_FOOTER: tuple = (
        f'[{Button.EDIT}] edit',
        f'[{Button.CANCEL}] cancel',
    )
