from typing import Any, Callable

from .decorators import frame
from .ioworkers import console
from .models import Contact


class MessagesInfo:

    main_menu_options: str = """
Options:
  number from 0 to 9 selects a contact from list;
  -a: add new contact;
  -n: next ten contacts from list;
  -p: previous ten contacts from list;
  -f: search contact;
  -l: fill contacts from file;
  -q: quit application.
"""

    create_contact_options: str = """
Options:
  1: add first name;
  2: add last name;
  3: add surname;
  4: add company;
  5: add work phone;
  6: add mobile phone;
  -s: save contact;
  -c: cancel operation;
  -q: quit application.
"""

    edit_contact_options: str = """
Options:
  1: edit first name;
  2: edit last name;
  3: edit surname;
  4: edit company;
  5: edit work phone;
  6: edit mobile phone;
  -s: update contact;
  -d: delete contact;
  -c: cancel operation;
  -q: quit application.
"""

    contact_detail_options: str = """
Options:
  -e: edit contact fields;
  -c: cancel operation;
  -q: quit application.
"""

    find_contacts_options: str = """
Options:
  number from 0 to 9 selects a contact from list;
  -f: retry search query;
  -c: cancel operation;
  -q: quit application.
"""


def help_message(handler_name: str) -> str:
    """Return help message about handler."""
    return getattr(MessagesInfo, handler_name)


class RenderMenuMessage:
    """Rendering menu messages."""

    @staticmethod
    def __render_contact_list(contacts: list[Contact], empty_msg: str) -> None:
        if not contacts:
            console.write(empty_msg.center(50, ' '))
            return

        sepr = console.sepr()
        for i, contact in enumerate(contacts):
            console.write(f'{i}: {contact.short_view}')
            if i < len(contacts) - 1:
                console.write(sepr)

    @staticmethod
    def __render_create_update_contact(contact: Contact) -> None:
        sepr = console.sepr()

        contact_data: dict = contact.model_dump(exclude_none=True)
        first_name: str = contact_data.get('first_name', 'First name')
        last_name: str = contact_data.get('last_name', 'Last name')
        surname: str = contact_data.get('surname', 'Surname')
        company: str = contact_data.get('company', 'Company')
        work: str = contact_data.get('work', 'Add work phone')
        modile: str = contact_data.get('mobile', 'Add mobile phone')

        text_message: str = (
            f'1. {first_name}\n{sepr}\n'
            f'2. {last_name}\n{sepr}\n'
            f'3. {surname}\n{sepr}\n'
            f'4. {company}\n{sepr}\n'
            f'5. {work}\n{sepr}\n'
            f'6. {modile}'
        )
        console.write(text_message)

    @frame(['Contacts'], ['add', 'search', 'quit'])
    @staticmethod
    def _render_main_menu(contacts: list[Contact]) -> None:
        RenderMenuMessage.__render_contact_list(contacts, 'No Contacts')

    @frame(['Search'], ['select', 'retry', 'cancel'])
    def _render_find_contacts(contacts: list[Contact]) -> None:
        RenderMenuMessage.__render_contact_list(contacts, 'No Results')

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
            'type -h (or --help) to display available commands: '
        )
    while action.lower() not in allowed_options:
        action = console.read(
            'No such option. '
            'Enter -h (or --help) to display available commands: '
        )
    return action
