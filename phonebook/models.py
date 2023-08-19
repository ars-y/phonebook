from pydantic import BaseModel


class ContactBaseModel(BaseModel):
    """Базовая модель контакта в телефонном справочнике."""

    _id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    surname: str | None = None
    company: str | None = None
    work: str | None = None
    mobile: str | None = None


class Contact(ContactBaseModel):
    """Модель контакта."""
    pass
