from .constants import FRAME_SIZE
from .ioworkers import console


def frame(headers: list[str], footers: list[str]):
    """Decorator to create header and footer frame."""
    def frame_decorator(func):
        def wrapper(*args, **kwargs):
            header: str = '| ' + ' | '.join(headers) + ' |'
            footer: str = '| ' + ' | '.join(footers) + ' |'

            console.write(header.center(FRAME_SIZE, '#'))
            console.write('\n')

            func(*args, **kwargs)

            console.write('\n')
            console.write(footer.center(FRAME_SIZE, '#'))
            console.write('\n')
        return wrapper
    return frame_decorator
