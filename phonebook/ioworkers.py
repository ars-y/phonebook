import os
import sys
from typing import Any


FIELD_SEP_LENGTH: int = 30


class ConsoleIO:
    """Interacts with console I/O."""

    def clear(self) -> None:
        """Clearing the terminal."""
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

    def exit(self) -> None:
        """Terminate the program."""
        self.clear()
        sys.exit()

    def write(self, data: Any) -> None:
        """Write the data to a stream."""
        print(data)

    def read(self, prompt: str = '') -> str:
        """Read a string from input."""
        return input(prompt)

    def click(self, continue_key: str = 'Press ENTER to continue ') -> None:
        """
        Print a message from argument `continue_key`
        and wait for any key to be entered.
        """
        self.read(continue_key)

    @staticmethod
    def sepr(sep_char: str = '-', length: int = FIELD_SEP_LENGTH) -> str:
        """Return separator."""
        return sep_char*length


console: ConsoleIO = ConsoleIO()
