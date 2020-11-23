from typing import Any

def safe_get(l: Any, i: int, default=None) -> Any:
    """Safely get an element from a list by its index"""
    try:
        return l[i]
    except TypeError:
        return default
    except IndexError:
        return default

def identity(x: Any) -> Any:
    """Identiy function"""
    return x

def natural_language(number: int) -> str:
    """Converts an int into its natural language representation"""
    return str(int(number))