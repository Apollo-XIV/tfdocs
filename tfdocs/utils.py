from result import as_result, Ok, Err, Result
from typing import Callable


def hello_world(name: str = "world") -> str:
    if name == "":
        name = "world"
    return f"hello, {name}!"


def try_wrap(f: Callable, *args, **kwargs) -> Result:
    """
    Wraps a function that can error with a Result type, allowing for safe
    type based error handling. This is best used in cases where a function
    can't return a critical error
    """
    try:
        return Ok(f(*args, **kwargs))
    except Exception as e:
        return Err(e)
