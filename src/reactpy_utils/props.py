from __future__ import annotations

import inspect
from types import FrameType
from typing import Any, cast


def props(include: str | None = None, exclude: str | None = None) -> dict[str, Any]:
    """Convert the caller functions arguments into a props dict. Include the arguments named
    in the include string. Exclude those named in the exclude string. If nether include or
    exclude are defined all the arguments are added to the props dict.

    Args:
        include (str, optional): Arguments to include in the returned props. Defaults to None.
        exclude (str, optional): Arguments to exclude from the returned props. Defaults to None.

    Returns:
        dict[str, Any]: The props

    Example:
    ```
    @component
    def Input(
        label: str | None = None,
        id: str | None = None,
        name: str | None = None,
        placeholder: str | None = None,
        value: str | None = None,
    ):
        _input_props = props(include="id, name, placeholder, value")
        return html.div(html.h2(label), html.input(_input_props))
    ```
    """

    frame: FrameType = cast(FrameType, cast(FrameType, inspect.currentframe()).f_back)

    all_args = frame.f_locals.copy()

    # Add all args if include is not defined or the none-zero include values

    _props: dict[str, Any] = {
        name: value for name, value in all_args.items() if not include or (name in include and value is not None)
    }

    # Drop any args in the exclude list

    if exclude:
        for name in list(_props):
            if name in exclude:
                _props.pop(name)

    return _props
