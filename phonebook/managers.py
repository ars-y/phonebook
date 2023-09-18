from typing import Callable

from . import handlers
from .constants import Button
from .models import Contact
from .render import Frame, FrameLabel, Render, RenderButtons


class MenuOptionManager:
    """Menu options manager."""

    def __init__(self) -> None:
        self._common_options: dict = {
            Button.QUIT: handlers.quit_app,
            Button.HELP: handlers.help_info,
            Button.HELP_L: handlers.help_info,
        }

    @property
    def main_menu_options(self) -> dict:
        self._common_options.update(
            {
                Button.ADD: handlers.create_contact,
                Button.FIND: handlers.search_query,
                Button.NEXT: handlers.page_changer,
                Button.PREV: handlers.page_changer,
            }
        )
        return self._common_options

    @property
    def create_contact_options(self) -> dict:
        self._common_options.update(
            {
                Button.SAVE: handlers.save_contact,
                Button.CANCEL: handlers.main_menu,
            }
        )
        return self._common_options

    @property
    def edit_contact_options(self) -> dict:
        self._common_options.update(
            {
                Button.DELETE: handlers.remove_contact,
                Button.SAVE: handlers.update_contact,
                Button.CANCEL: handlers.contact_detail,
            }
        )
        return self._common_options

    @property
    def contact_detail_options(self) -> dict:
        self._common_options.update(
            {
                Button.EDIT: handlers.edit_contact,
                Button.CANCEL: handlers.main_menu,
            }
        )
        return self._common_options

    @property
    def find_contacts_options(self) -> dict:
        self._common_options.update(
            {
                Button.FIND: handlers.search_query,
                Button.CANCEL: handlers.main_menu,
                Button.NEXT: handlers.page_changer,
                Button.PREV: handlers.page_changer,
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


class RenderManager:
    """Rendering manager."""

    def __init__(self, data: dict) -> None:
        self.render: Render = Render(data)

    def _render_main_menu(self) -> None:
        if isinstance(self.render.data, dict):
            current_page: int = self.render.data.get('page')
            total_pages: int = self.render.data.get('total_pages')
            contacts: list[Contact] = self.render.data.get('contacts')

            render_buttons = RenderButtons(FrameLabel.MAIN_FOOTER)
            render_buttons.page_changer(current_page, total_pages)
            render_buttons.select_contact(contacts)

        self.render.frame = Frame(
            FrameLabel.MAIN_HEADER,
            [*FrameLabel.MAIN_FOOTER.values()]
        )
        self.render.contact_list(empty_msg='No Contacts')

    def _render_find_contacts(self) -> None:
        if isinstance(self.render.data, dict):
            current_page: int = self.render.data.get('page')
            total_pages: int = self.render.data.get('total_pages')
            contacts: list[Contact] = self.render.data.get('contacts')

            render_buttons = RenderButtons(FrameLabel.FIND_FOOTER)
            render_buttons.page_changer(current_page, total_pages)
            render_buttons.select_contact(contacts)

        self.render.frame = Frame(
            FrameLabel.FIND_HEADER,
            [*FrameLabel.FIND_FOOTER.values()]
        )
        self.render.contact_list(empty_msg='No Results')

    def _render_create_contact(self) -> None:
        if isinstance(self.render.data, dict):
            render_buttons = RenderButtons(FrameLabel.CREATE_FOOTER)
            render_buttons.save_contact(self.render.data.get('contact'))

        self.render.frame = Frame(
            FrameLabel.CREATE_HEADER,
            [*FrameLabel.CREATE_FOOTER.values()]
        )
        self.render.create_edit_contact()

    def _render_edit_contact(self) -> None:
        if isinstance(self.render.data, dict):
            render_buttons = RenderButtons(FrameLabel.EDIT_FOOTER)
            render_buttons.save_contact(self.render.data.get('contact'))

        self.render.frame = Frame(
            FrameLabel.EDIT_HEADER,
            [*FrameLabel.EDIT_FOOTER.values()]
        )
        self.render.create_edit_contact()

    def _render_contact_detail(self) -> None:
        self.render.frame = Frame(
            FrameLabel.DETAIL_HEADER,
            [*FrameLabel.DETAIL_FOOTER]
        )
        self.render.create_edit_contact(short_view=True)

    def _render_help_message(self) -> None:
        self.render.frame = Frame(FrameLabel.HELP_HEADER)
        self.render._render_window()


def render(handler: Callable, data: dict) -> None:
    """Render menu depending on handler."""
    attr_name: str = '_render_' + handler.__name__
    _render = getattr(RenderManager(data), attr_name)
    _render()
