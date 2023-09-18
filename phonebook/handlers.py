"""
The logic of the app is built on event handlers
that receive content from the context.

Context content:
    * handler:
        - meaning: event handler;
        - type: Callable.
    * callback:
        - meaning: value that led into the handler;
        - type: str.
    * contact_list:
        - meaning: list of Contact models;
        - type: list[Contact].
    * Contact model:
        > contact:
            - meaning: Contact model;
            - type: Contact.
        > old_contact:
            - meaning: Contact model before update;
            - type: Contact.
        > field:
            - meaning: Contact field name;
            - type: depends on the Contact field type.
        > value:
            - meaning: value for Contact field;
            - type: depends on the Contact field type.
    * searching:
        > search_result:
            - meaning: list of found Contact models;
            - type: list[Contact]
        > query:
            - meaning: query string to find a contact
            in contact list;
            - type: str.
    * state:
        - meaning: report on the operation of add,
        updade or delete a contact;
        - type: str.
    * pagination:
        > page:
            - meaning: current page;
            - type: int.
        > per_page:
            - type: int.
        > total_pages:
            - type: int.
"""
from typing import Callable

from .constants import PAGE_SIZE, Button, ReportState
from .ioworkers import console
from .managers import get_allowed_options, render
from .messages import help_message, request_action, print_report
from .models import Contact, TOTAL_FIELDS
from .storages import PhoneBook
from .utils import (
    calc_total_pages,
    get_paginate_bound,
    remove_item,
    remove_keys_from_dict,
)
from .validators import validate_field


def main_menu(context: dict) -> None:
    """
    Main menu handler.
    Display a list contacts sorted by name.

    Available:
        - pagination contacts;
        - add new contact;
        - select contact from list;
        - search contact;
        - quit application.
    """
    console.clear()

    context['handler'] = main_menu
    contacts: list[Contact] = context.get('contact_list')
    options: dict = get_allowed_options(main_menu)

    begin, end = get_paginate_bound(
        page=context.get('page'),
        per_page=context.get('per_page'),
        total_pages=context.get('total_pages')
    )
    contacts_per_page: list = contacts[begin:end]
    options.update(
        **dict.fromkeys(
            (str(i) for i in range(1, len(contacts_per_page) + 1)),
            contact_detail
        )
    )

    render_data: dict = {
        'page': context.get('page'),
        'total_pages': context.get('total_pages'),
        'contacts': contacts_per_page
    }
    render(main_menu, render_data)

    if 'state' in context:
        print_report(context.get('state'))

    action: str = request_action(options)

    if 'state' in context:
        del context['state']

    if action == Button.FIND:
        context['page'] = 1
    else:
        context['callback'] = action

    if (
        action.isdigit()
        and int(action) in range(1, len(contacts_per_page) + 1)
    ):
        contact = contacts_per_page[int(action) - 1]
        context['contact'] = contact

    console.clear()
    options[action.lower()](context)


def create_update_contact(context: dict) -> None:
    """Generic handler for creating and updating contact fields."""
    console.clear()

    handler: str = context.get('handler')
    contact: Contact = context.get('contact', Contact())
    total_fields = range(1, TOTAL_FIELDS + 1)
    options: dict = get_allowed_options(handler)
    options.update(**dict.fromkeys((str(i) for i in total_fields), set_field))

    if contact.is_empty:
        options.pop(Button.SAVE)

    render(handler, {'contact': contact})
    action: str = request_action(options)

    if action.isdigit() and int(action) in total_fields:
        fileds: dict = dict(zip(total_fields, contact.model_fields))
        field = fileds[int(action)]
        value = console.read('Enter value: ')

        if field in ('mobile', 'work'):
            value = validate_field(value)

        context['field'] = field
        context['value'] = value

    if action == Button.CANCEL:
        if handler is not edit_contact:
            context['contact'] = Contact()
        else:
            context['contact'] = context.get('old_contact', contact)

    else:
        context['contact'] = contact

    contacts: list = context.get('contact_list')
    context['total_pages'] = calc_total_pages(
        contacts, context.get('per_page')
    )

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
    callback: str = context.get('callback')

    context['handler'] = contact_detail
    options: dict = get_allowed_options(contact_detail)

    render(contact_detail, {'contact': context.get('contact')})
    action: str = request_action(options)

    if action == Button.CANCEL:
        if 'contact' in context:
            context['contact'] = Contact()

        if callback == find_contacts.__name__:
            options.update({Button.CANCEL: find_contacts})

    console.clear()
    options[action.lower()](context)


def search_query(context: dict) -> None:
    """Request a search string."""
    console.clear()

    search_string: str = console.read('Enter a search string: ')
    if not search_string:
        contacts: list = context.get('contact_list')
        context['total_pages'] = calc_total_pages(
            contacts, context.get('per_page')
        )
        main_menu(context)

    context['query'] = search_string
    find_contacts(context)


def find_contacts(context: dict) -> None:
    """
    Handler for searching contacts.

    Available:
        - pagination contacts;
        - retry search request;
        - cancel operation.
    """
    console.clear()

    context['handler'] = find_contacts
    options: dict = get_allowed_options(find_contacts)
    search_string: str = context.get('query')

    phone_book: PhoneBook = PhoneBook()

    if 'search_result' in context:
        contacts: list[Contact] = context.get('search_result')
    else:
        contacts: list[Contact] = phone_book.find_all(search_string)
        context['search_result'] = contacts

    begin, end = get_paginate_bound(
        page=context.get('page'),
        per_page=context.get('per_page'),
        total_pages=context.get('total_pages')
    )
    contacts_per_page: list = contacts[begin:end]

    total_pages: int = calc_total_pages(contacts, context.get('per_page'))
    context['total_pages'] = total_pages

    render_data: dict = {
        'page': context.get('page'),
        'total_pages': total_pages,
        'contacts': contacts_per_page,
    }
    render(find_contacts, render_data)

    if not contacts:
        console.write(f'Search string: {search_string}')

    options.update(
        **dict.fromkeys(
            (str(i) for i in range(1, len(contacts_per_page) + 1)),
            contact_detail
        )
    )

    action: str = request_action(options)

    if action not in (Button.PREV, Button.NEXT):
        if action in (Button.CANCEL, Button.FIND):
            context.pop('search_result')

        contacts: list = context.get('contact_list')
        context.update(
            {
                'page': 1,
                'total_pages': calc_total_pages(
                    contacts, context.get('per_page')
                ),
                'callback': find_contacts.__name__
            }
        )

    else:
        context['callback'] = action

    if (
        action.isdigit()
        and int(action) in range(1, len(contacts_per_page) + 1)
    ):
        contact = contacts_per_page[int(action) - 1]
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

    if not field_value.isspace():
        temp = contact.model_copy(deep=True)
        setattr(temp, field_name, field_value)
        context['contact'] = temp

        if 'old_contact' not in context:
            context['old_contact'] = contact

    handler(context)


def help_info(context: dict) -> None:
    """Handler for printing help info about menu."""
    handler: Callable = context.get('handler')
    help_message(handler)
    console.clear()
    handler(context)


def connect_database(context: dict, mode: str) -> None:
    """
    Connects to the database and applies operations
    depending on the selected mode.
    """
    contact: Contact = context.get('contact')
    contacts: list[Contact] = context.get('contact_list')
    old_contact: Contact | None = None
    state: str = ReportState.DONOTHING

    if 'old_contact' in context:
        old_contact = context['old_contact']
        del context['old_contact']

    if contact.is_empty and not old_contact:
        context['state'] = ReportState.DECLINE
        return

    phone_book: PhoneBook = PhoneBook(contact)

    if mode.startswith('save') and contact not in contacts:
        phone_book.save()
        contacts.append(contact)
        state = ReportState.ACCEPT

    elif mode.startswith('update') and old_contact:
        phone_book.update()
        contacts = remove_item(contacts, old_contact)
        contacts.append(contact)
        state = ReportState.ACCEPT

    elif mode.startswith('remove'):
        phone_book.remove()

        if old_contact:
            contacts = remove_item(contacts, old_contact)
        else:
            contacts = remove_item(contacts, contact)

        state = ReportState.ACCEPT

    keys_to_remove: tuple = (
        'callback',
        'field',
        'handler',
        'query',
        'search_result',
        'value',
    )
    remove_keys_from_dict(keys_to_remove, context)
    context.update(
        {
            'contact': Contact(),
            'contact_list': contacts,
            'page': 1,
            'total_pages': calc_total_pages(
                contacts, context.get('per_page')
            ),
            'state': state,
        }
    )


def run_app():
    """Running application in cycle."""
    contacts: list[Contact] = PhoneBook().load()
    context: dict = {
            'page': 1,
            'per_page': PAGE_SIZE,
            'total_pages': calc_total_pages(contacts, PAGE_SIZE),
            'contact_list': contacts,
    }

    while True:
        main_menu(context)


def quit_app(context: dict | None = None):
    """Escape from application."""
    console.exit()
