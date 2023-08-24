from pathlib import Path


BASE_DIR: Path = Path(__file__).resolve().parent.parent

CONTACTS_DIR: Path = BASE_DIR / 'files'

CONTACTS_FILE: Path = CONTACTS_DIR / 'contacts.csv'

DB_DIR: Path = BASE_DIR / 'data'

DB_PATH: str = str(DB_DIR / 'contacts.db')

FILE_INIT_KEY: str = '--init'

UPLOAD_FILE_KEY: str = '--upload'

PAGE_SIZE: int = 6


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
