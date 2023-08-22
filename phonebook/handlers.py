from typing import Callable

from .storages import PhoneBook
from .models import Contact
from .messages import help_message, render, request_action
from .ioworkers import console
from .validators import validate_field


PAGE_SIZE: int = 10


# TODO: make pagination
def main_menu(context: dict | None = None) -> None:
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

    context: dict = context or {}
    context['handler'] = main_menu

    phone_book: PhoneBook = PhoneBook()
    contacts: list[Contact] = context.get(
        'contact_list', phone_book.load()
    )

    options: dict = {
        '-a': create_contact,
        '-f': search_query,
        '-q': quit_app,
        '-h': help_info,
        '--help': help_info,
    }
    contacts_per_page: list = contacts[:PAGE_SIZE]
    options.update(
        **dict.fromkeys(
            (str(i) for i in range(len(contacts_per_page))), contact_detail
        )
    )

    render(main_menu, contacts)

    action: str = request_action(options)

    if action.isdigit() and int(action) in range(len(contacts_per_page)):
        contact = contacts_per_page[int(action)]
        context['contact'] = contact

    console.clear()
    options[action.lower()](context)


def create_update_contact(
    context: dict | None = None,
    *,
    mode: str | None = None
) -> None:
    """Generic handler for creating and updating contact fields."""
    handler: str = context.get('handler')

    digits = range(1, 7)
    options: dict = {
        '-q': quit_app,
        '-h': help_info,
        '--help': help_info,
    }
    options.update(**dict.fromkeys((str(i) for i in digits), set_field))

    if mode.startswith('create'):
        options.update(
            {
                '-s': save_contact,
                '-c': main_menu,
            }
        )
    else:
        options.update(
            {
                '-d': remove_contact,
                '-s': update_contact,
                '-c': contact_detail,
            }
        )

    contact: Contact = context.get('contact', Contact())
    render(handler, contact)
    action: str = request_action(options)

    if action.isdigit() and int(action) in digits:
        fileds: dict = dict(zip(digits, contact.model_fields))
        field = fileds[int(action)]
        value = console.read('Enter value: ')

        if field in ('mobile', 'work'):
            value = validate_field(value)

        if not value:
            create_contact(context)

        context['field'] = field
        context['value'] = value

    context['contact'] = contact

    console.clear()
    options[action.lower()](context)


def create_contact(context: dict | None = None) -> None:
    """
    Handler for creating contact.

    Available:
        - add contact fields;
        - cancel operation.
    """
    context['handler'] = create_contact
    create_update_contact(context, mode=create_contact.__name__)


def edit_contact(context: dict | None = None) -> None:
    """
    Handler for editing contact fields.

    Available:
        - select contact field to edit;
        - delete contact;
        - cancel operation.
    """
    context['handler'] = edit_contact
    create_update_contact(context, mode=edit_contact.__name__)


def contact_detail(context: dict | None = None):
    """
    Handler for viewing contact detail.

    Available:
        - edit contact fields;
        - cancel operation.
    """
    context['handler'] = contact_detail

    options: dict = {
        '-e': edit_contact,
        '-c': main_menu,
        '-q': quit_app,
        '-h': help_info,
        '--help': help_info,
    }

    render(contact_detail, context.get('contact'))
    action: str = request_action(options)

    if action == '-c' and 'contact' in context:
        context['contact'] = Contact()

    console.clear()
    options[action.lower()](context)


def search_query(context: dict | None = None) -> None:
    """Request a search string."""
    console.clear()

    search_string: str = console.read('Enter a search string: ')
    if search_string == '-c':
        main_menu()

    context['query'] = search_string
    find_contacts(context)


def find_contacts(context: dict | None = None) -> None:
    """
    Handler for searching contacts.

    Available:
        - retry search request;
        - cancel operation.
    """
    console.clear()

    context['handler'] = find_contacts
    options: dict = {
        '-f': search_query,
        '-c': main_menu,
        '-q': quit_app,
        '-h': help_info,
        '--help': help_info,
    }

    search_string: str = context.get('query')
    phone_book: PhoneBook = PhoneBook()
    contacts: list[Contact] = phone_book.find_all(search_string)

    render(find_contacts, contacts)

    if not contacts:
        console.write(f'Search string: {search_string}')

    options.update(
        **dict.fromkeys(
            (str(i) for i in range(len(contacts))), contact_detail
        )
    )

    action: str = request_action(options)
    if action.isdigit() and int(action) in range(len(contacts)):
        contact = contacts[int(action)]
        context['contact'] = contact

    console.clear()
    options[action.lower()](context)


def save_contact(context: dict | None = None) -> None:
    """Handler for saving contact in DB."""
    contact: Contact = context.get('contact')
    if not contact.is_empty:
        phone_book: PhoneBook = PhoneBook(contact)
        phone_book.save()


def update_contact(context: dict | None = None) -> None:
    """Handler for update contact in DB."""
    contact: Contact = context.get('contact')
    if not contact.is_empty:
        phone_book: PhoneBook = PhoneBook(contact)
        phone_book.update()


def remove_contact(context: dict | None = None) -> None:
    """Handler for remove contact from DB."""
    contact: Contact = context.get('contact')
    if not contact.is_empty:
        phone_book: PhoneBook = PhoneBook(contact)
        phone_book.remove()


def set_field(context: dict | None = None) -> None:
    """Handler for setting value in model field."""
    handler: Callable = context.get('handler')
    contact: Contact = context.get('contact')
    field_name: str = context.get('field')
    field_value: str = context.get('value')

    setattr(contact, field_name, field_value)
    context['contact'] = contact
    handler(context)


def help_info(context: dict | None = None) -> None:
    """Handler for printing help info about menu."""
    handler: Callable = context.get('handler')
    handler_name: str = handler.__name__ + '_options'
    console.write(help_message(handler_name))
    console.read('Press ENTER to continue ')
    console.clear()
    handler(context)


def run_app():
    """Running application in cycle."""
    while True:
        main_menu()


def quit_app(context: dict | None = None):
    """Escape from application."""
    console.exit()
