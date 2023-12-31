from pydantic import BaseModel

from .ioworkers import console
from .utils import concat_dict_values


class ContactBaseModel(BaseModel):
    """Base Contact model."""

    _id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    surname: str | None = None
    company: str | None = None
    mobile: str | None = None
    work: str | None = None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            this: dict = self.model_dump(
                exclude_none=True, exclude_unset=True
            )
            other: dict = other.model_dump(
                exclude_none=True, exclude_unset=True
            )

            return all(
                [
                    other.get(key, '').lower() == this[key].lower()
                    for key in this
                ]
            )

        return super().__eq__(other)


class Contact(ContactBaseModel):
    """Contact model."""

    @property
    def card_view(self) -> str:
        """Card view of the contact model."""
        sepr: str = console.sepr()
        empty_value: str = ''

        _first_name: str = self.first_name if self.first_name else empty_value
        _last_name: str = self.last_name if self.last_name else empty_value
        _surname: str = self.surname if self.surname else empty_value
        _company: str = self.company if self.company else empty_value
        _mobile: str = self.mobile if self.mobile else empty_value
        _work: str = self.work if self.work else empty_value

        contact_card: str = (
            f'First name: {_first_name}\n{sepr}\n'
            f'Last name: {_last_name}\n{sepr}\n'
            f'Surname: {_surname}\n{sepr}\n'
            f'Company: {_company}\n{sepr}\n'
            f'Mobile: {_mobile}\n{sepr}\n'
            f'Work: {_work}'
        )
        return contact_card

    @property
    def short_view(self) -> str:
        """
        Brief view of the contact model.
        Return first not None field value.
        """
        if self.first_name and self.last_name:
            return ' '.join([self.first_name, self.last_name])

        if self.first_name and self.company:
            return ' '.join([self.first_name, self.company])

        if self.last_name and self.company:
            return ' '.join([self.last_name, self.company])

        model_as_dict: dict[str, str] = self.model_dump()
        for field in model_as_dict:
            if model_as_dict[field]:
                return model_as_dict[field]

    @property
    def is_empty(self) -> bool:
        return not concat_dict_values(
            self.model_dump(exclude_none=True, exclude_unset=True)
        )


TOTAL_FIELDS: int = len(Contact.model_fields)
