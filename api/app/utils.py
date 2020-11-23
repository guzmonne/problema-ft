from typing import Any
from .models.value import Value

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

def add_natural_language(value: Value) -> Value:
    """Adds a natural_language key to a value object"""
    if value is None:
        return
    value["natural_language"] = "uni"
    return value    
    