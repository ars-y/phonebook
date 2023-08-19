def concat_dict_values(data: dict) -> str:
    """Конкатенация всех значений словаря."""
    return ''.join(
        str(value).replace(' ', '').lower() for value in data.values()
    )
