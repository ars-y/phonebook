from typing import Callable

from .constants import FIRST, LAST, Button
from .ioworkers import console
from .managers import render
from .models import TOTAL_FIELDS


def _get_numbered_fields(fileds_names: tuple, mode: str) -> str:
    numbered_fields: list = []
    for number, field in zip(range(1, TOTAL_FIELDS + 1), fileds_names):
        numbered_fields.append(f'  {number}: {mode} {field};')

        if number < TOTAL_FIELDS:
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

    main_menu_options: str = f"""Options:
  number from {FIRST} to {LAST} selects a contact from list;
  [{Button.ADD}]: add new contact;
  [{Button.NEXT}]: next page;
  [{Button.PREV}]: previous page;
  [{Button.FIND}]: search contact;
  [{Button.QUIT}]: quit application."""

    create_contact_options: str = f"""Options:
{__add_fields}
  [{Button.SAVE}]: save contact;
  [{Button.CANCEL}]: cancel operation;
  [{Button.QUIT}]: quit application."""

    edit_contact_options: str = f"""Options:
{__edit_fields}
  [{Button.SAVE}]: update contact;
  [{Button.DELETE}]: delete contact;
  [{Button.CANCEL}]: cancel operation;
  [{Button.QUIT}]: quit application."""

    contact_detail_options: str = f"""Options:
  [{Button.EDIT}]: edit contact fields;
  [{Button.CANCEL}]: cancel operation;
  [{Button.QUIT}]: quit application."""

    find_contacts_options: str = f"""Options:
  number from {FIRST} to {LAST} selects a contact from list;
  [{Button.NEXT}]: next page;
  [{Button.PREV}]: previous page;
  [{Button.FIND}]: retry search query;
  [{Button.CANCEL}]: cancel operation;
  [{Button.QUIT}]: quit application."""


def help_message(handler: Callable) -> None:
    """Print help message about handler."""
    handler_name: str = handler.__name__ + '_options'
    help_text: str = getattr(MessagesInfo, handler_name)
    render(help_message, help_text)
    console.click()


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


def print_report(state: str) -> None:
    """Print database interaction report."""
    console.write(state)
