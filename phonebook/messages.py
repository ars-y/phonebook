from typing import Any, Callable

from .constants import PAGE_SIZE, Button
from .decorators import frame
from .ioworkers import console
from .models import Contact


first, *_, last = range(PAGE_SIZE)


def _get_numbered_fields(fileds_names: tuple, mode: str) -> str:
    total_fields: int = len(Contact.model_fields)
    numbered_fields: list = []
    for number, field in zip(range(1, total_fields + 1), fileds_names):
        numbered_fields.append(f'  {number}: {mode} {field};')

        if number < total_fields:
            numbered_fields.append('\n')

    return ''.join(numbered_fields)


class MessagesInfo:
    """Help message store."""

    __fields_names: tuple = (
        'first name', 'last name', 'surname',
        'company', 'work phone', 'mobile phone'
    )

    __add_fields: str = _get_numbered_fields(__fields_names, 'add')
    __edit_fields: str = _get_numbered_fields(__fields_names, 'edit')

    main_menu_options: str = f"""
Options:
  number from {first} to {last} selects a contact from list;
  [{Button.ADD}]: add new contact;
  [{Button.NEXT}]: next page;
  [{Button.PREV}]: previous page;
  [{Button.FIND}]: search contact;
  [{Button.QUIT}]: quit application.
"""

    create_contact_options: str = f"""
Options:
{__add_fields}
  [{Button.SAVE}]: save contact;
  [{Button.CANCEL}]: cancel operation;
  [{Button.QUIT}]: quit application.
"""

    edit_contact_options: str = f"""
Options:
{__edit_fields}
  [{Button.SAVE}]: update contact;
  [{Button.DELETE}]: delete contact;
  [{Button.CANCEL}]: cancel operation;
  [{Button.QUIT}]: quit application.
"""

    contact_detail_options: str = f"""
Options:
  [{Button.EDIT}]: edit contact fields;
  [{Button.CANCEL}]: cancel operation;
  [{Button.QUIT}]: quit application.
"""

    find_contacts_options: str = f"""
Options:
  number from {first} to {last} selects a contact from list;
  [{Button.NEXT}]: next page;
  [{Button.PREV}]: previous page;
  [{Button.FIND}]: retry search query;
  [{Button.CANCEL}]: cancel operation;
  [{Button.QUIT}]: quit application.
"""


def help_message(handler_name: str) -> str:
    """Return help message about handler."""
    return getattr(MessagesInfo, handler_name)


class RenderMenuMessage:
    """Rendering menu messages."""

    @staticmethod
    def __render_contact_list(
        data: tuple[list[Contact, int, int]],
        empty_msg: str
    ) -> None:
        contacts, current_page, total_pages = data

        if not contacts:
            console.write(empty_msg.center(50, ' '))
            return

        sepr = console.sepr()
        for i, contact in enumerate(contacts):
            console.write(f'{i}: {contact.short_view}')
            if i < len(contacts) - 1:
                console.write(sepr)

        if total_pages:
            console.write(f'Page: {current_page}/{total_pages}'.rjust(50, ' '))

    @staticmethod
    def __render_create_update_contact(contact: Contact) -> None:
        sepr = console.sepr()

        first_name: str = contact.first_name if contact.first_name else 'First name'
        last_name: str = contact.last_name if contact.last_name else 'Last name'
        surname: str = contact.surname if contact.surname else 'Surname'
        company: str = contact.company if contact.company else 'Company'
        modile: str = contact.mobile if contact.mobile else 'Add mobile phone'
        work: str = contact.work if contact.work else 'Add work phone'

        text_message: str = (
            f'1. {first_name}\n{sepr}\n'
            f'2. {last_name}\n{sepr}\n'
            f'3. {surname}\n{sepr}\n'
            f'4. {company}\n{sepr}\n'
            f'5. {modile}\n{sepr}\n'
            f'6. {work}'
        )
        console.write(text_message)

    @frame(['Contacts'], ['next', 'prev', 'add', 'find', 'quit'])
    @staticmethod
    def _render_main_menu(data: tuple[list[Contact, int, int]]) -> None:
        RenderMenuMessage.__render_contact_list(data, 'No Contacts')

    @frame(['Search'], ['next', 'prev', 'select', 'find', 'cancel'])
    def _render_find_contacts(data: tuple[list[Contact, int, int]]) -> None:
        RenderMenuMessage.__render_contact_list(data, 'No Results')

    @frame(['New Contact'], ['select', 'save', 'cancel'])
    @staticmethod
    def _render_create_contact(contact: Contact) -> None:
        RenderMenuMessage.__render_create_update_contact(contact)

    @frame(['Edit Contact'], ['select', 'save', 'delete', 'cancel'])
    @staticmethod
    def _render_edit_contact(contact: Contact) -> None:
        RenderMenuMessage.__render_create_update_contact(contact)

    @frame(['Contact detail'], ['edit', 'cancel'])
    @staticmethod
    def _render_contact_detail(contact: Contact) -> None:
        console.write(contact.card_view)


def render(handler: Callable, data: Any) -> None:
    """Render menu depending on handler."""
    attr_name: str = '_render_' + handler.__name__
    _render = getattr(RenderMenuMessage, attr_name)
    _render(data)


def request_action(allowed_options: dict) -> str:
    """Allowed action request."""
    action: str = console.read(
            'Select action or '
            'type h (or help) to display available commands: '
        )
    while action.lower() not in allowed_options:
        action = console.read(
            'No such option. '
            'Enter h (or help) to display available commands: '
        )
    return action
