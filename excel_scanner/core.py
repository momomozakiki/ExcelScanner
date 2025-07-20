def normalize_text(value):
    if isinstance(value, str):
        return value.strip().lower()
    return value


def format_position(row, col):
    return f"R{row}C{col}"