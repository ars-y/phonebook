import argparse
import os
from pathlib import Path

from .constants import CONTACTS_DIR, DB_DIR, FILE_INIT_KEY, UPLOAD_FILE_KEY
from .storages import PhoneBook


def files_init() -> None:
    """Initialize file structure."""
    path_list: tuple = (CONTACTS_DIR, DB_DIR)
    for path in path_list:
        if not dir_is_exists(path):
            make_dir(path)


def make_dir(path: str | Path) -> None:
    """Create directory."""
    os.mkdir(path)


def dir_is_exists(path: str | Path) -> bool:
    """Checking if a directory exists."""
    return os.path.isdir(path)


def argument_parser() -> None:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Contact management application'
    )
    parser.add_argument(
        FILE_INIT_KEY,
        action='store_true',
        help='initialize file structure (*required for the first run)'
    )
    parser.add_argument(
        UPLOAD_FILE_KEY,
        type=Path,
        metavar='PATH',
        help='loading contacts data from file'
    )

    args = parser.parse_args()

    if args.init:
        files_init()

    if args.upload:
        PhoneBook().upload_from(args.upload)
