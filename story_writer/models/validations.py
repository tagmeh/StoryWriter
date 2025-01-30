def str_not_empty(value: str) -> str:
    """Prevents empty strings from being a valid input when requiring a string input."""
    value = value.strip()
    if value == "":
        raise ValueError(f"'{value}' must not be empty.")
    return value
