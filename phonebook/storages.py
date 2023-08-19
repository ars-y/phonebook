import csv
import shelve
from pathlib import Path

from .constants import CONTACTS_FILE, DB_NAME
from .models import ContactBaseModel


class BasePhoneBook:
    """Базовая модель телефонного справочника."""

    def __init__(self, contact: ContactBaseModel | None = None) -> None:
        self._contact = contact

    def save(self, *, flush: bool = True) -> None:
        """
        Сохраняет контакт в базу данных, после
        чего сбрасывает данные в файл,
        если ключевой не имеет значения False.

        Аргументы:
            - **flush**: булевский аргумент,
            который сбрасывает контакты в файл
            если значение True (по умолчанию)
        """
        with shelve.open(DB_NAME) as db:
            db[self._contact._id] = self._contact
        if flush:
            self.flush()

    def load(self) -> list:
        """Выгружает список контактов из файла."""
        data: list = []
        with shelve.open(DB_NAME) as db:
            for key in db:
                data.append(db[key])
        return data

    def find(self, patterns: list[str]) -> ContactBaseModel:
        """Находит контакт в записной книжке по характеристикам."""

    def flush(self, filename: str | Path = CONTACTS_FILE) -> None:
        """
        Сбрасывает контакт в текстовый файл для хранения контактов.
        Если имя файла или путь не указаны, то используется
        указанный по умолчанию.

        Аргументы:
            - **filename**: путь до файла.
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

    def remove(self, *, flush: bool = True) -> None:
        """Удаляет запись из базы данных."""
        with shelve.open(DB_NAME) as db:
            key = self._contact._id
            if key in db:
                del db[key]
        if flush:
            self.flush()

    def update(self):
        """Обновляет данные контакта."""

    def __str__(self) -> str:
        pass


class PhoneBook(BasePhoneBook):
    """Модель телефонного справочника."""
    pass
