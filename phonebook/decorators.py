from typing import Callable

from .constants import FRAME_SIZE
from .ioworkers import console


def frame(
    headers: list[str] | None = None,
    footers: list[str] | None = None
) -> Callable:
    """Decorator to create header and footer frame."""
    def frame_decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> None:
            header: str = '| ' + ' | '.join(headers) + ' |' if headers else ''
            footer: str = '| ' + ' | '.join(footers) + ' |' if footers else ''

            console.write(header.center(FRAME_SIZE, '#'))
            console.write('\n')

            func(*args, **kwargs)

            console.write('\n')
            console.write(footer.center(FRAME_SIZE, '#'))
            console.write('\n')
        return wrapper
    return frame_decorator
