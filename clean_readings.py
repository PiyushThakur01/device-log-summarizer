"""Section 1: clean and normalize sensor readings."""
from typing import Any, Iterable, List

MAX_VALUE = 500.0


def clean_readings(values: Iterable[Any]) -> List[float]:
    """Convert to float, drop invalid/None/negative values, clip at 500.0."""
    cleaned: List[float] = []
    for value in values or []:
        if value is None or isinstance(value, bool):
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if number != number or number < 0:  # NaN or negative error flag
            continue
        cleaned.append(min(number, MAX_VALUE))
    return cleaned
