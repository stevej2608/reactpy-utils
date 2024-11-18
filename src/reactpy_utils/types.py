from typing import Any, Callable

EventArgs = dict[str, Any]

EventHandler = Callable[[EventArgs], None]

Action = Callable[..., None]

Props = dict[str, Any]


def NO_PROPS() -> dict[str, Any]:
    return {}


PropsFunc = Callable[..., dict[str, Any]]
