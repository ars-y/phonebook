class MessagesInfo:

    main_menu_option: str = """
The following options are available:
- number from 0 to 9 selects a contact from list;
- A: add new contact;
- N: next ten contacts from list;
- P: previous ten contacts from list;
- S: search contact;
- L: fill contacts from file;
- Q: quit application.
"""


def help_message(handler_name: str) -> str:
    """Return help message about handler."""
    return getattr(MessagesInfo, handler_name)
