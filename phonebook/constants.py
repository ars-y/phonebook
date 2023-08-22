from pathlib import Path


BASE_DIR: Path = Path(__file__).resolve().parent.parent

CONTACTS_DIR: Path = BASE_DIR / 'files'

CONTACTS_FILE: Path = CONTACTS_DIR / 'contacts.csv'

DB_DIR: Path = BASE_DIR / 'data'

DB_PATH: str = str(DB_DIR / 'contacts.db')
