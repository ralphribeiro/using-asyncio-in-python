# A utility function for coercing input into a list
from typing import Any


def listify(x: Any) -> list:
    """Try hard to convert x into a list."""
    if isinstance(x, (str, bytes)):
        return [x]
    
    try:
        return [_ for _ in x]
    except TypeError:
        return [x]