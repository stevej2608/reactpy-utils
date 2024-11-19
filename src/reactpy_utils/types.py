from typing import Any, Callable

EventArgs = dict[str, Any]
"""Event handler args type"""

EventHandler = Callable[[EventArgs], None]
"""Event handler type"""

Action = Callable[..., None]
"""A callable type that returns None"""

Props = dict[str, Any]
"""A props dict type"""

PropsFunc = Callable[..., dict[str, Any]]
"""A callable type that returns a props dict"""


def NO_PROPS() -> dict[str, Any]:
    """A function that returns an empty props dict"""
    return {}
