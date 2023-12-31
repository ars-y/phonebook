import sys

from phonebook import argument_parser, FILE_INIT_KEY
from phonebook import run_app


def main():
    try:
        run_app()
    except OSError as exc:
        exc_message: str = str(exc)
        if exc_message.startswith('[Errno 2]'):
            exc_info: str = (
                '\nIf you are running application for the first time, '
                f'use key [{FILE_INIT_KEY}] '
                'to create the necessary directories.\n'
            )
            exc_message += exc_info

        sys.stdout.write(exc_message)
        sys.exit(1)


if __name__ == '__main__':

    major, minor, *_ = sys.version_info
    if major < 3 and minor < 10:
        sys.stdout.write(
            'Python version below 3.10 isn\'t currently supported'
        )
        sys.exit()

    if len(sys.argv) > 1:
        argument_parser()

    main()
