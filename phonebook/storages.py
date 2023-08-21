import csv
import shelve
from pathlib import Path

from .constants import CONTACTS_FILE, DB_NAME
from .models import Contact
from .utils import concat_dict_values


class BasePhoneBook:
    """Base model of the Phonebook."""

    def __init__(self, contact: Contact | None = None) -> None:
        self._contact = contact

    def save(
        self,
        filename: str | Path = DB_NAME,
        *,
        flush: bool = True
    ) -> None:
        """
        Saving Contact object in DB.
        Flush contacts from DB to text file if `flush` True.

        Args:
            - **filename**: name of file or path to file;
            - **flush**: key argument - boolean flag
            for flush contacts from DB to text file.
        """
        with shelve.open(filename) as db:
            if not self._contact._id:
                self._contact._id = self.__generate_id()

            db[self._contact._id] = self._contact

        if flush:
            self.flush()

    def load(
        self,
        filename: str | Path = DB_NAME,
        *,
        contact_id: str = None,
        multiple: bool = True
    ) -> Contact | list:
        """
        Fetch contacts list from DB.
        Return single Contact object if multiple flag is False
        and passed contact ID (if exists in DB).

        Args:
            - **filename**: name of file or path to file;
            - **contact_id**: key argument - contact ID;
            - **multiple**: key argument - boolean flag
            to fetch all contacts in list.
        """
        data: list = []
        with shelve.open(filename) as db:
            if not multiple:
                return db.get(contact_id)

            for key in db:
                data.append(db[key])

        return data

    def flush(self, filename: str | Path = CONTACTS_FILE) -> None:
        """
        Flush contacts from DB to text file.
        Default path to file taken from constants module.

        Args:
            - **filename**: name of file or path to file.
        """
        contacts: list[Contact] = self.load()
        with open(filename, 'w', encoding='utf-8') as f:
            rows: list[dict] = [
                contact.model_dump() for contact in contacts
            ]
            row: dict = self._contact.model_dump()
            if row not in rows:
                rows.append(row)

            writer = csv.DictWriter(f, row.keys())
            writer.writerows(rows)

    def remove(
        self,
        filename: str | Path = DB_NAME,
        *,
        contact_id: str = None,
        flush: bool = True
    ) -> None:
        """
        Remove contact from DB.

        Args:
            - **filename**: name of file or path to file;
            - **contact_id**: key argument - contact ID;
            - **flush**: key argument - boolean flag
            for flush contacts from DB to text file.
        """
        with shelve.open(filename) as db:
            key = self._contact._id if not contact_id else contact_id
            if key in db:
                del db[key]

        if flush:
            self.flush()

    def upload_from(self, filename: str | Path, _type: str = 'csv') -> None:
        """
        Loading contacts data from file.

        Args:
            - **filename**: name of file or path to file;
            - **_type**: file extension.
        """
        load_handlers: dict = {
            'csv': self.__loader_csv,
        }
        load_handlers[_type](filename)

    def __loader_csv(self, filename: str | Path):
        """Loader data from csv file."""
        with open(filename, 'r', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                self._contact: Contact = Contact(
                    first_name=row.get('first_name'),
                    last_name=row.get('last_name'),
                    surname=row.get('surname'),
                    company=row.get('company'),
                    work=row.get('work'),
                    mobile=row.get('mobile')
                )
                self.save(flush=False)

    def __generate_id(self) -> str:
        """Generate contact ID."""
        return concat_dict_values(
            self._contact.model_dump(exclude_unset=True)
        )

    def __str__(self) -> str:
        pass


class PhoneBook(BasePhoneBook):
    """Model of the Phonebook."""

    def __init__(self, contact: Contact | None = None) -> None:
        super().__init__(contact)

    def find(self, contact_id: str) -> Contact | None:
        """Find Contact object by ID and return it."""
        return self.load(contact_id=contact_id, multiple=False)

    def find_all(self, pattern: str) -> list[Contact]:
        """Find contacts by pattern."""

    def update(self) -> None:
        """Update Contact data in DB."""
        old_contact: Contact | None = self.find(self._contact._id)

        # TODO: make exception for not exists contact ID
        if not old_contact:
            raise KeyError('ID not exists')

        self.remove(contact_id=old_contact._id, flush=False)
        self.save()
