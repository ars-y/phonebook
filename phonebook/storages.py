import csv
import shelve
from pathlib import Path

from .constants import CONTACTS_FILE, DB_NAME
from .models import Contact
from .utils import concat_dict_values


class BasePhoneBook:
    """Базовая модель телефонного справочника."""

    def __init__(self, contact: Contact | None = None) -> None:
        self._contact = contact

    def save(
        self,
        filename: str | Path = DB_NAME,
        *,
        flush: bool = True
    ) -> None:
        """
        Сохраняет контакт в базу данных, после
        чего сбрасывает данные в файл,
        если ключевой не имеет значения False.

        Аргументы:
            - **filename**: имя или путь до файла для хранения;
            - **flush**: ключевой аргумент,
            флаг для сбрасывания контактов в текстовый файл.
        """
        with shelve.open(filename) as db:
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
        Выгружает список контактов из файла.
        Вернет объект контакта, если убран флаг multiple
        и задан ID контакта, при наличии его в базе данных.

        Аргументы:
            - **filename**: имя или путь до файла для хранения;
            - **contact_id**: ключевой аргумент ID контакта;
            - **multiple**: ключевой аргумент,
            флаг для выгрузки списка контактов.
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
        Сбрасывает контакт в текстовый файл для хранения контактов.
        Если имя файла или путь не указаны, то используется
        указанный по умолчанию.

        Аргументы:
            - **filename**: имя или путь до файла для хранения;
        """
        contacts: list = self.load()
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
        Удаляет запись из базы данных.

        Аргументы:
            - **filename**: имя или путь до файла для хранения;
            - **contact_id**: ключевой аргумент ID контакта;
            - **flush**: ключевой аргумент,
            флаг для сбрасывания контактов в текстовый файл.
        """
        with shelve.open(filename) as db:
            key = self._contact._id if not contact_id else contact_id
            if key in db:
                del db[key]

        if flush:
            self.flush()

    def __str__(self) -> str:
        pass


class PhoneBook(BasePhoneBook):
    """Модель телефонного справочника."""

    def __init__(self, contact: Contact | None = None) -> None:
        super().__init__(contact)

    def find(self, contact_id: str) -> Contact | None:
        """Возвращает объект контакта пo его ID."""
        return self.load(contact_id=contact_id, multiple=False)

    def find_all(self, patterns: list[str]) -> list[Contact]:
        """Возвращает список контактов, по заданным критериям."""

    def update(self) -> None:
        """Обновляет данные контакта."""
        old_contact: Contact | None = self.find(self._contact._id)
        if not old_contact:
            raise KeyError('данного контакта не существует')

        self.remove(contact_id=old_contact._id, flush=False)
        self._contact._id: str = concat_dict_values(
            self._contact.model_dump(exclude_unset=True)
        )
        self.save()
