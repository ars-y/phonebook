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
    """Checking that elements contain a target value using binary search."""
    def binary_search(
        elements: list,
        target: str,
        left: int,
        right: int
    ) -> bool:
        if left > right:
            return False

        middle: int = (left + right) // 2

        if target in elements[middle]:
            return True

        if target > elements[middle]:
            return binary_search(elements, target, middle + 1, right)

        return binary_search(elements, target, left, middle - 1)

    if not _unique:
        elements: list = [element for element in elements if element]

    if not _sort:
        elements.sort()

    return binary_search(elements, target, 0, len(elements) - 1)
