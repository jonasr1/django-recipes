from typing import SupportsFloat


def is_positive_number(value: SupportsFloat) -> bool:
    try:
        number_string = float(value)
    except (TypeError, ValueError):
        return False
    return number_string > 0
