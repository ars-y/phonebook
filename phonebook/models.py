from pydantic import BaseModel
from .utils import field_separator


class ContactBaseModel(BaseModel):
    """Base Contact model."""

    _id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    surname: str | None = None
    company: str | None = None
    work: str | None = None
    mobile: str | None = None


class Contact(ContactBaseModel):
    """Contact model."""

    @property
    def card_view(self) -> str:
        """Card view of the contact model."""
        contact_card: list = []
        sepr: str = field_separator()

        if self.first_name:
            contact_card.append(f'First name: {self.first_name}{sepr}')

        if self.last_name:
            contact_card.append(f'Last name: {self.last_name}{sepr}')

        if self.surname:
            contact_card.append(f'Surname: {self.surname}{sepr}')

        if self.company:
            contact_card.append(f'Company: {self.company}{sepr}')

        if self.work:
            contact_card.append(f'Mobile: {self.work}{sepr}')

        if self.mobile:
            contact_card.append(f'Work: {self.mobile}{sepr}')

        return ''.join(contact_card)

    @property
    def short_view(self) -> str:
        """
        Brief view of the contact model.
        Return first not None field value.
        """
        fields: dict = self.model_dump()
        for name in fields:
            if fields[name]:
                return fields[name]
