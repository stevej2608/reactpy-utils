from __future__ import annotations

import inspect
from types import FrameType
from typing import Any, cast


def props(include: str = "", exclude: str = "") -> dict[str, Any]:
    """Convert the caller functions arguments into a props dict

    Args:
        include (str, optional): Arguments to include in the returned props. Defaults to ''.
        exclude (str, optional): Arguments to exclude from the returned props. Defaults to ''.

    Returns:
        Dict[str, Any]: The props
    """

    frame: FrameType | None = cast(FrameType, inspect.currentframe()).f_back

    if not frame:
        err = "Unable to resolve calling function"
        raise TypeError(err)

    all_args = frame.f_locals.copy()

    _props: dict[str, Any] = {
        name: value for name, value in all_args.items() if not include or (name in include and value is not None)
    }

    if exclude:
        for name in list(_props):
            if name in exclude:
                _props.pop(name)

    return _props
