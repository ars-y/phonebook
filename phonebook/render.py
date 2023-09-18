from .constants import (
    FRAME_DESIGN,
    FRAME_SIZE,
    FIRST,
    LAST,
    FIRST_FIELD,
    LAST_FIELD,
    Button
)
from .ioworkers import console
from .models import Contact
from .utils import get_eges


class FrameLabel:
    """Labels for frames."""

    HELP_HEADER: str = 'Help Info'
    MAIN_HEADER: str = 'Contacts'
    MAIN_FOOTER: dict = {
        'prev': f'[{Button.PREV}] prev',
        'next': f'[{Button.NEXT}] next',
        'select': f'[{FIRST}-{LAST}] select',
        'add': f'[{Button.ADD}] add',
        'find': f'[{Button.FIND}] find',
        'quit': f'[{Button.QUIT}] quit',
    }
    FIND_HEADER: str = 'Search'
    FIND_FOOTER: dict = {
        'prev': f'[{Button.PREV}] prev',
        'next': f'[{Button.NEXT}] next',
        'select': f'[{FIRST}-{LAST}] select',
        'find': f'[{Button.FIND}] find',
        'cancel': f'[{Button.CANCEL}] cancel',
        'quit': f'[{Button.QUIT}] quit',
    }
    CREATE_HEADER: str = 'New Contact'
    CREATE_FOOTER: dict = {
        'select': f'[{FIRST_FIELD}-{LAST_FIELD}] select',
        'save': f'[{Button.SAVE}] save',
        'cancel': f'[{Button.CANCEL}] cancel',
    }
    EDIT_HEADER: str = 'Edit Contact'
    EDIT_FOOTER: dict = {
        'select': f'[{FIRST_FIELD}-{LAST_FIELD}] select',
        'save': f'[{Button.SAVE}] save',
        'delete': f'[{Button.DELETE}] delete',
        'cancel': f'[{Button.CANCEL}] cancel',
    }
    DETAIL_HEADER: str = 'Contact detail'
    DETAIL_FOOTER: tuple = (
        f'[{Button.EDIT}] edit',
        f'[{Button.CANCEL}] cancel',
    )


class Frame:
    """
    Frame render.
    Gets a list titles and available options
    for rendering  the frame header and footer.
    """

    def __init__(
        self,
        titles: list[str] | str | None = None,
        options: list[str] | str | None = None
    ) -> None:
        self.headers: list[str] | str | None = titles
        self.footers: list[str] | str | None = options

    def render_header(self) -> None:
        """Render frame header."""
        if not self.headers:
            header: str = ''
        elif isinstance(self.headers, list):
            header: str = '| ' + ' | '.join(self.headers) + ' |'
        else:
            header: str = '| ' + self.headers + ' |'

        console.write(header.center(FRAME_SIZE, FRAME_DESIGN))
        console.write('\n')

    def render_footer(self) -> None:
        """Render frame footer."""
        footers = self.footers
        if not footers:
            footer: str = ''
        elif isinstance(footers, list):
            footer: str = '| ' + ' | '.join(f for f in footers if f) + ' |'
        else:
            footer: str = '| ' + footers + ' |'

        console.write('\n')
        console.write(footer.center(FRAME_SIZE, FRAME_DESIGN))
        console.write('\n')


class Render:
    """
    Application window rendering.
    Gets the render data and frame instance to render window.
    """

    def __init__(
        self,
        render_data: dict | str,
        frame: Frame | None = None
    ) -> None:
        self.data = render_data
        self.frame = frame

    def _render_window(self, to_render: str | None = None) -> None:
        if not to_render and isinstance(self.data, str):
            to_render = self.data

        self.frame.render_header()
        console.write(to_render)
        self.frame.render_footer()

    def contact_list(self, empty_msg: str = '') -> None:
        to_render: list = []
        contacts: list[Contact] = self.data.get('contacts')
        current_page: int = self.data.get('page')
        total_pages: int = self.data.get('total_pages')

        if not contacts:
            self._render_window(empty_msg.center(FRAME_SIZE, ' '))
            return

        sepr = console.sepr()
        for i, contact in enumerate(contacts, start=1):
            to_render.append(f'{i}: {contact.short_view}')
            if i < len(contacts):
                to_render.append(sepr)

        if total_pages:
            to_render.append(
                f'Page: {current_page}/{total_pages}'.rjust(
                    FRAME_SIZE, ' '
                )
            )

        self._render_window('\n'.join(to_render))

    def create_edit_contact(self, short_view: bool = False) -> None:
        to_render: list = []
        contact: Contact = self.data.get('contact')

        if short_view:
            self._render_window(contact.card_view)
            return

        sepr = console.sepr()

        first_name: str = (
            contact.first_name
            if contact.first_name
            else 'First name'
        )
        last_name: str = (
            contact.last_name
            if contact.last_name
            else 'Last name'
        )
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
        to_render.append(text_message)

        self._render_window('\n'.join(to_render))


class RenderButtons:
    """Render available buttons."""

    def __init__(self, buttons: dict, hide_button: str = '') -> None:
        self.buttons = buttons
        self.hide_button = hide_button

    def page_changer(
        self,
        current_page: int,
        total_pages: int
    ) -> None:
        """
        Hides or show the page change buttons depending on the
        current page and the total number of pages.
        """
        if not total_pages or total_pages == 1:
            self.buttons.update(
                {'prev': self.hide_button, 'next': self.hide_button}
            )

        elif current_page == 1 and current_page < total_pages:
            self.buttons.update(
                {'prev': self.hide_button, 'next': f'[{Button.NEXT}] next'}
            )

        elif 1 < current_page < total_pages:
            self.buttons.update(
                {
                    'prev': f'[{Button.PREV}] prev',
                    'next': f'[{Button.NEXT}] next'
                }
            )

        elif current_page == total_pages:
            self.buttons.update(
                {'prev': f'[{Button.PREV}] prev', 'next': self.hide_button}
            )

    def save_contact(self, contact: Contact) -> None:
        """
        Hides or show the save button depending on
        Contact model is empty or not.
        """
        if contact.is_empty:
            self.buttons['save'] = self.hide_button
            return

        self.buttons['save'] = f'[{Button.SAVE}] save'

    def select_contact(self, contacts: list[Contact]) -> None:
        """
        Hides or show the contact selection button depending on
        the number of contacts in the list.
        """
        amount_contacts: int = len(contacts)

        if not contacts:
            self.buttons['select'] = self.hide_button
            return

        if amount_contacts <= 1:
            self.buttons['select'] = f'[{amount_contacts}] select'
            return

        first, last = get_eges(amount_contacts)
        self.buttons['select'] = f'[{first}-{last}] select'
