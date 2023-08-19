import os
from pathlib import Path

from .constants import CONTACTS_DIR, DB_DIR


def files_init() -> None:
    """Инициализация файловой структуры."""
    path_list: tuple = (CONTACTS_DIR, DB_DIR)
    for path in path_list:
        if not dir_is_exists(path):
            make_dir(path)


def make_dir(path: str | Path) -> None:
    """Создание директории, если её не существует."""
    os.mkdir(path)


def dir_is_exists(path: str | Path) -> bool:
    """Проверка существования директории"""
    return os.path.isdir(path)
