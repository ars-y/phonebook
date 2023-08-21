from typing import Callable

from .storages import PhoneBook
from .models import Contact
from .messages import help_message, render, request_action
from .ioworkers import console
from .validators import validate


PAGE_SIZE: int = 10


def main_menu(context: dict | None = None):
    """
    Main menu handler.
    Display a list contacts sorted by name.

    Available:
        - pagination with 10 contacts per page;
        - select contact from list;
        - search contact;
        - add new contact;
        - quit application.
    """
    console.clear()

    phone_book: PhoneBook = PhoneBook()
    contacts: list[Contact] = phone_book.load()

    options: dict = {
        '-a': create_contact,
        '-f': find_contact,
        '-q': quit_app,
        '-h': help_info,
        '--help': help_info,
    }
    contacts_per_page: list = contacts[:PAGE_SIZE]
    options.update(
        **dict.fromkeys(
            (str(i) for i in range(len(contacts_per_page))), set_field
        )
    )

    render(main_menu, contacts)

    action: str = request_action(options)

    # TODO: make pagination
    if action.isdigit() and int(action) in len(contacts_per_page):
        ...

    console.clear()
    options[action.lower()]({'handler': main_menu})


def create_contact(context: dict | None = None):
    """
    Обработчик создания контакта.
    Доступные действия:
        - добавления указанных полей контакта.
        - отмена операции создания контакта.
    """
    digits = range(1, 7)

    context['handler'] = create_contact
    options: dict = {
        '-s': save_contact,
        '-c': main_menu,
        '-h': help_info,
        '--help': help_info,
    }
    options.update(**dict.fromkeys((str(i) for i in digits), set_field))

    contact: Contact = context.get('contact', Contact())
    render(create_contact, contact)
    action: str = request_action(options)

    if action.isdigit() and int(action) in digits:
        fileds: dict = dict(zip(digits, contact.model_fields))
        field = fileds[int(action)]
        value = console.read('Enter value: ')

        if field in ('mobile', 'work'):
            value = validate(field, value)

        context['field'] = field
        context['value'] = value

    context['contact'] = contact

    console.clear()
    options[action.lower()](context)


def edit_contact(context: dict | None = None):
    """
    Обработчик изменения полей контакта.
    Доступные действия:
        - выбрать поле, которое необходимо изменить/добавить;
        - полностью удаленить контакт;
        - отмена операции изменения контакта.
    """


def find_contact(context: dict | None = None):
    """
    Обработчик поиска контакта.
    Доступные действия:
        - указание одного или несколько значений,
        по которым должен произвестись поиск;
        - отмена операции изменения контакта.
    """


def save_contact(context: dict | None = None):
    """Save contact in DB handler."""
    contact: Contact = context.get('contact')
    phone_book: PhoneBook = PhoneBook(contact)
    phone_book.save()


def set_field(context: dict | None = None):
    """Set value in model field."""
    handler: Callable = context.get('handler')
    contact: Contact = context.get('contact')
    field_name: str = context.get('field')
    field_value: str = context.get('value')

    setattr(contact, field_name, field_value)
    context['contact'] = contact
    handler(context)


def help_info(context: dict | None = None):
    """Print help info about menu handler."""
    handler: Callable = context.get('handler')
    handler_name: str = handler.__name__ + '_options'
    console.write(help_message(handler_name))
    console.read('Press ENTER to continue ')
    handler(context)


def run_app():
    """Running application in cycle."""
    while True:
        main_menu()


def quit_app(context: dict | None = None):
    """Escape from application."""
    exit()
