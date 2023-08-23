from typing import Any


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


def replace_item(items: list, value: Any) -> list:
    """
    Return a new list with item replaced by the new value.

    Args:
        - **items**: list object;
        - **value**: any type that can be compared.
    """
    return [value if item == value else item for item in items]


def remove_item(items: list, value: Any) -> list:
    """
    Return a new list without old value.

    Args:
        - **items**: list object;
        - **value**: any type that can be compared.
    """
    return [item for item in items if item != value]
