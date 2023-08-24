from typing import Callable

from .constants import PAGE_SIZE, Button
from .ioworkers import console
from .messages import help_message, render, request_action
from .models import Contact
from .storages import PhoneBook
from .utils import (
    calc_total_pages,
    get_paginate_bound,
    replace_item,
    remove_item
)
from .validators import validate_field


def main_menu(context: dict) -> None:
    """
    Main menu handler.
    Display a list contacts sorted by name.

    Available:
        - pagination with 10 contacts per page;
        - add new contact;
        - select contact from list;
        - search contact;
        - quit application.
    """
    console.clear()

    context['handler'] = main_menu
    contacts: list[Contact] = context.get('contact_list')
    options: dict = get_allowed_options(main_menu)

    begin, end = get_paginate_bound(context)
    contacts_per_page: list = contacts[begin:end]
    options.update(
        **dict.fromkeys(
            (str(i) for i in range(len(contacts_per_page))), contact_detail
        )
    )

    current_page: int = context.get('page')
    total_pages: int = context.get('total_pages')
    render_data: tuple = (
        contacts_per_page, current_page, total_pages
    )
    render(main_menu, render_data)

    action: str = request_action(options)
    if action == Button.FIND:
        context['page'] = 1
    else:
        context['callback'] = action

    if action.isdigit() and int(action) in range(len(contacts_per_page)):
        contact = contacts_per_page[int(action)]
        context['contact'] = contact

    console.clear()
    options[action.lower()](context)


def create_update_contact(context: dict) -> None:
    """Generic handler for creating and updating contact fields."""
    console.clear()

    handler: str = context.get('handler')
    contact: Contact = context.get('contact', Contact())
    total_fields = range(1, len(contact.model_fields) + 1)
    options: dict = get_allowed_options(handler)
    options.update(**dict.fromkeys((str(i) for i in total_fields), set_field))

    render(handler, contact)
    action: str = request_action(options)

    if action.isdigit() and int(action) in total_fields:
        fileds: dict = dict(zip(total_fields, contact.model_fields))
        field = fileds[int(action)]
        value = console.read('Enter value: ')

        if field in ('mobile', 'work'):
            value = validate_field(value)

        context['field'] = field
        context['value'] = value

    if action == Button.CANCEL and handler is not edit_contact:
        context['contact'] = Contact()
    else:
        context['contact'] = contact

    contacs: list = context.get('contact_list')
    context['total_pages'] = calc_total_pages(contacs)

    console.clear()
    options[action.lower()](context)


def create_contact(context: dict) -> None:
    """
    Handler for creating contact.

    Available:
        - add contact fields;
        - cancel operation.
    """
    context['handler'] = create_contact
    create_update_contact(context)


def edit_contact(context: dict) -> None:
    """
    Handler for editing contact fields.

    Available:
        - select contact field to edit;
        - delete contact;
        - cancel operation.
    """
    context['handler'] = edit_contact
    create_update_contact(context)


def contact_detail(context: dict):
    """
    Handler for viewing contact detail.

    Available:
        - edit contact fields;
        - cancel operation.
    """
    context['handler'] = contact_detail
    options: dict = get_allowed_options(contact_detail)

    render(contact_detail, context.get('contact'))
    action: str = request_action(options)

    if action == Button.CANCEL and 'contact' in context:
        context['contact'] = Contact()

    console.clear()
    options[action.lower()](context)


def search_query(context: dict) -> None:
    """Request a search string."""
    console.clear()

    search_string: str = console.read('Enter a search string: ')
    if not search_string:
        contacs: list = context.get('contact_list')
        context['total_pages'] = calc_total_pages(contacs)
        main_menu(context)

    context['query'] = search_string
    find_contacts(context)


def find_contacts(context: dict) -> None:
    """
    Handler for searching contacts.

    Available:
        - retry search request;
        - cancel operation.
    """
    console.clear()

    context['handler'] = find_contacts
    options: dict = get_allowed_options(find_contacts)
    search_string: str = context.get('query')

    phone_book: PhoneBook = PhoneBook()
    contacts: list[Contact] = phone_book.find_all(search_string)
    begin, end = get_paginate_bound(context)
    contacts_per_page: list = contacts[begin:end]

    total_pages: int = calc_total_pages(contacts)
    context['total_pages'] = total_pages

    current_page: int = context.get('page')
    render_data: tuple = (
        contacts_per_page, current_page, total_pages
    )
    render(find_contacts, render_data)

    if not contacts:
        console.write(f'Search string: {search_string}')

    options.update(
        **dict.fromkeys(
            (str(i) for i in range(len(contacts_per_page))), contact_detail
        )
    )

    action: str = request_action(options)

    if action == Button.CANCEL:
        context['page'] = 1
        contacts: list = context.get('contact_list')
        context['total_pages'] = calc_total_pages(contacts)

    else:
        context['callback'] = action

    if action.isdigit() and int(action) in range(len(contacts_per_page)):
        contact = contacts_per_page[int(action)]
        context['contact'] = contact

    console.clear()
    options[action.lower()](context)


def save_contact(context: dict) -> None:
    """Handler for saving contact in DB."""
    connect_database(context, save_contact.__name__)


def update_contact(context: dict) -> None:
    """Handler for update contact in DB."""
    connect_database(context, update_contact.__name__)


def remove_contact(context: dict) -> None:
    """Handler for remove contact from DB."""
    connect_database(context, remove_contact.__name__)


def page_changer(context: dict) -> None:
    """Move to the next or previous page."""
    action: str = context.get('callback')
    current_page = context.get('page')
    total_pages: int = context.get('total_pages')
    handler: Callable = context.get('handler')

    if action == Button.NEXT and current_page < total_pages:
        current_page += 1

    if action == Button.PREV and current_page > 1:
        current_page -= 1

    context['page'] = current_page
    handler(context)


def set_field(context: dict) -> None:
    """Handler for setting value in model field."""
    handler: Callable = context.get('handler')
    contact: Contact = context.get('contact')
    field_name: str = context.get('field')
    field_value: str = context.get('value')

    if field_value:
        setattr(contact, field_name, field_value)
        context['contact'] = contact

    handler(context)


def help_info(context: dict) -> None:
    """Handler for printing help info about menu."""
    handler: Callable = context.get('handler')
    handler_name: str = handler.__name__ + '_options'
    console.write(help_message(handler_name))
    console.read('Press ENTER to continue ')
    console.clear()
    handler(context)


class MenuOptionManager:
    """Menu options manager."""

    def __init__(self) -> None:
        self._common_options: dict = {
            Button.QUIT: quit_app,
            Button.HELP: help_info,
            Button.HELP_L: help_info,
        }

    @property
    def main_menu_options(self) -> dict:
        self._common_options.update(
            {
                Button.ADD: create_contact,
                Button.FIND: search_query,
                Button.NEXT: page_changer,
                Button.PREV: page_changer,
            }
        )
        return self._common_options

    @property
    def create_contact_options(self) -> dict:
        self._common_options.update(
            {
                Button.SAVE: save_contact,
                Button.CANCEL: main_menu,
            }
        )
        return self._common_options

    @property
    def edit_contact_options(self) -> dict:
        self._common_options.update(
            {
                Button.DELETE: remove_contact,
                Button.SAVE: update_contact,
                Button.CANCEL: contact_detail,
            }
        )
        return self._common_options

    @property
    def contact_detail_options(self) -> dict:
        self._common_options.update(
            {
                Button.EDIT: edit_contact,
                Button.CANCEL: main_menu,
            }
        )
        return self._common_options

    @property
    def find_contacts_options(self) -> dict:
        self._common_options.update(
            {
                Button.FIND: search_query,
                Button.CANCEL: main_menu,
                Button.NEXT: page_changer,
                Button.PREV: page_changer,
            }
        )
        return self._common_options


def get_allowed_options(handler: Callable) -> dict:
    """
    Return a dict with allowed menu options
    depending on the handler passed in arguments.
    """
    attr_name: str = handler.__name__ + '_options'
    return getattr(MenuOptionManager(), attr_name)


def connect_database(context: dict, mode: str) -> None:
    """
    Connects to the database and applies operations
    depending on the selected mode.
    """
    contact: Contact = context.get('contact')
    contacts: list[Contact] = context.get('contact_list')
    if contact.is_empty:
        return

    phone_book: PhoneBook = PhoneBook(contact)

    if mode.startswith('save'):
        phone_book.save()
        contacts.append(contact)

    elif mode.startswith('update'):
        phone_book.update()
        contacts = replace_item(contacts, contact)

    elif mode.startswith('remove'):
        phone_book.remove()
        contacts = remove_item(contacts, contact)

    context['contact'] = Contact()
    context['contact_list'] = contacts
    context['page'] = 1
    context['total_pages'] = calc_total_pages(contacts)


def run_app():
    """Running application in cycle."""
    context: dict = {}
    contacts: list[Contact] = PhoneBook().load()

    context['page'] = 1
    context['per_page'] = PAGE_SIZE
    context['total_pages'] = calc_total_pages(contacts)
    context['contact_list'] = contacts

    while True:
        main_menu(context)


def quit_app(context: dict | None = None):
    """Escape from application."""
    console.exit()
