from typing import Any

def safe_get(l: Any, i: int, default) -> Any:
    try:
        return l[i]
    except TypeError:
        return default
    except IndexError:
        return default
