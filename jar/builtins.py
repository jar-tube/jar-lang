"""Built-in functions for JAR language."""

from typing import Any, Dict, Callable


def builtin_print(*args):
    """Print values to stdout."""
    output = ' '.join(str(arg) for arg in args)
    print(output)
    return None


def builtin_len(obj: Any) -> int:
    """Get the length of a value."""
    if hasattr(obj, '__len__'):
        return len(obj)
    raise TypeError(f"object of type '{type(obj).__name__}' has no len()")


def builtin_type(obj: Any) -> str:
    """Get the type of a value."""
    if obj is None:
        return "null"
    elif isinstance(obj, bool):
        return "boolean"
    elif isinstance(obj, int) or isinstance(obj, float):
        return "number"
    elif isinstance(obj, str):
        return "string"
    elif isinstance(obj, list):
        return "list"
    elif isinstance(obj, dict):
        return "object"
    else:
        return "unknown"


def builtin_str(obj: Any) -> str:
    """Convert a value to a string."""
    if isinstance(obj, str):
        return obj
    elif obj is None:
        return "null"
    elif isinstance(obj, bool):
        return "true" if obj else "false"
    else:
        return str(obj)


def builtin_num(obj: Any) -> float:
    """Convert a value to a number."""
    if isinstance(obj, (int, float)):
        return obj
    elif isinstance(obj, str):
        try:
            if '.' in obj:
                return float(obj)
            return int(obj)
        except ValueError:
            raise ValueError(f"Cannot convert '{obj}' to number")
    elif isinstance(obj, bool):
        return 1 if obj else 0
    else:
        raise TypeError(f"Cannot convert {type(obj).__name__} to number")


def builtin_int(obj: Any) -> int:
    """Convert a value to an integer."""
    return int(builtin_num(obj))


def builtin_bool(obj: Any) -> bool:
    """Convert a value to a boolean."""
    if obj is None or obj is False:
        return False
    if obj == 0 or obj == "" or obj == [] or obj == {}:
        return False
    return True


def builtin_list(*args) -> list:
    """Create a list from arguments."""
    return list(args)


def builtin_range(*args) -> list:
    """Create a range of numbers."""
    if len(args) == 1:
        return list(range(int(args[0])))
    elif len(args) == 2:
        return list(range(int(args[0]), int(args[1])))
    elif len(args) == 3:
        return list(range(int(args[0]), int(args[1]), int(args[2])))
    else:
        raise TypeError(f"range() takes 1 to 3 arguments ({len(args)} given)")


def builtin_input(prompt: str = "") -> str:
    """Read input from user."""
    return input(prompt)


def builtin_push(lst: list, *values) -> None:
    """Add values to the end of a list."""
    if not isinstance(lst, list):
        raise TypeError(f"push() requires a list, got {type(lst).__name__}")
    lst.extend(values)
    return None


def builtin_pop(lst: list, index: int = -1) -> Any:
    """Remove and return an element from a list."""
    if not isinstance(lst, list):
        raise TypeError(f"pop() requires a list, got {type(lst).__name__}")
    if len(lst) == 0:
        raise IndexError("pop from empty list")
    return lst.pop(index)


def builtin_join(lst: list, separator: str = "") -> str:
    """Join list elements into a string."""
    if not isinstance(lst, list):
        raise TypeError(f"join() requires a list, got {type(lst).__name__}")
    return separator.join(str(item) for item in lst)


def builtin_split(string: str, separator: str = " ") -> list:
    """Split a string into a list."""
    if not isinstance(string, str):
        raise TypeError(f"split() requires a string, got {type(string).__name__}")
    if separator == "":
        return list(string)
    return string.split(separator)


def get_builtin_functions() -> Dict[str, Callable]:
    """Return a dictionary of all built-in functions."""
    return {
        'print': builtin_print,
        'len': builtin_len,
        'type': builtin_type,
        'str': builtin_str,
        'num': builtin_num,
        'int': builtin_int,
        'bool': builtin_bool,
        'list': builtin_list,
        'range': builtin_range,
        'input': builtin_input,
        'push': builtin_push,
        'pop': builtin_pop,
        'join': builtin_join,
        'split': builtin_split,
    }
