def concat_dict_values(data: dict) -> str:
    """Concatenation of all dict values in single string."""
    return ''.join(
        str(value).replace(' ', '').lower() for value in data.values()
    )
