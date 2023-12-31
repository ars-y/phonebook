from typing import Any, Iterable


def concat_dict_values(data: dict) -> str:
    """Concatenation of all dict values in single string."""
    return ''.join(
        str(value).replace(' ', '').lower() for value in data.values()
    )


def contains(
    elements: list[str],
    target: str,
    *,
    _sort: bool = False,
    _unique: bool = False
) -> bool:
    """
    Checking that elements contain a target value using binary search.

    Args:
        - **elements**: list with str objects inside;
        - **target**: value to be found in str;
        - **_sort**: key argument - boolean flag,
        make sorted list if it's False (default);
        - **_unique**: key argument - boolean flag,
        remove duplicates from list if it's False (default).
    """
    def binary_search(
        elements: list[str],
        target: str,
        left: int,
        right: int
    ) -> bool:
        if left > right:
            return False

        middle: int = (left + right) // 2

        element: str = elements[middle].lower()

        if target in element:
            return True

        if target > element:
            return binary_search(elements, target, middle + 1, right)

        return binary_search(elements, target, left, middle - 1)

    if not _unique:
        elements: list = [element for element in elements if element]

    if not _sort:
        elements.sort()

    return binary_search(elements, target, 0, len(elements) - 1)


def remove_item(items: list, value: Any) -> list:
    """
    Return a new list without old value.

    Args:
        - **items**: list object;
        - **value**: any type that can be compared.
    """
    return [item for item in items if item != value]


def get_paginate_bound(**data: dict) -> tuple[int, int]:
    """Return slice boundaries."""
    current_page: int = data.get('page')
    per_page: int = data.get('per_page')
    total_pages: int = data.get('total_pages')

    if 1 <= current_page <= total_pages:
        begin: int = (current_page - 1)*per_page
        end: int = current_page*per_page

        return begin, end

    return 0, per_page


def calc_total_pages(items: list, per_page: int) -> int:
    """
    Return the total number of pages
    based on total items and page size.
    """
    return (len(items) + per_page - 1) // per_page


def get_eges(length: int) -> tuple[int, int]:
    """Returns the first and last value of a range."""
    if length <= 2:
        return 1, length

    first, *_, second = range(1, length + 1)
    return first, second


def remove_keys_from_dict(keys: Iterable, context: dict) -> None:
    """Removes keys from a dictionary."""
    for key in keys:
        context.pop(key, None)
