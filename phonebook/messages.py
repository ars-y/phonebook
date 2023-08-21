from typing import Any, Callable

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
  -c: cancel operation.
"""


def help_message(handler_name: str) -> str:
    """Return help message about handler."""
    return getattr(MessagesInfo, handler_name)


class RenderMenuMessage:
    """Rendering menu messages."""

    @staticmethod
    def _render_main_menu(contacts: list[Contact]) -> None:
        if not contacts:
            console.write('No contacts')
            return

        console.write('| Contacts |'.center(50, '#'))
        console.write('\n')

        sepr = console.sepr()
        for i, contact in enumerate(contacts):
            console.write(f'{i}: {contact.short_view}')
            if i < len(contacts) - 1:
                console.write(sepr)

        console.write('\n')
        console.write('| add | search | quit |'.center(50, '#'))

    @staticmethod
    def _render_create_contact(contact: Contact) -> None:
        console.write('| New Contact |'.center(50, '#'))
        console.write('\n')

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
            f'6. {modile}\n'
        )
        console.write(text_message)
        console.write(''.center(50, '#'))


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
