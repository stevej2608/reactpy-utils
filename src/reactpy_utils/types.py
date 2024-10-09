from typing import Dict, Any, Callable

EventArgs = Dict[str, Any]

EventHandler  = Callable[[EventArgs], None]

Action = Callable[..., None]

Props = Dict[str, Any]

def NO_PROPS() -> Dict[str, Any]:
    return {}

PropsFunc = Callable[...,Dict[str, Any]]
