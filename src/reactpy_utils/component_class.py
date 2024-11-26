from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, cast

from reactpy.core.component import Component

if TYPE_CHECKING:
    from reactpy.core.types import VdomDict

NONE = cast(Any, None)


class _ComponentClass(Component):
    """Base class for all ComponentClass implementations"""

    def __init__(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]):
        super().__init__(function=self.render, key=NONE, args=args, kwargs=kwargs, sig=NONE)

    def render(self) -> VdomDict:
        raise NotImplementedError


def class_component(comp: type):
    """ReactPy ComponentClass decorator

    Args:
        comp (Type): Class to be wrapped

    Usage:
    ```
        from reactpy import html, run
        from reactpy_utils  import class_component

        @class_component
        class HelloWorld:

            def render(self):
                return html.h2('Hello World!')

        run(HelloWorld)
    ```
    """

    comp = type(comp.__name__, (comp, _ComponentClass), {})
    sig = inspect.signature(comp)

    def create_component(*args: Any, key: Any | None = None, **kwargs: Any) -> Component:
        _comp = comp(*args, **kwargs)
        _comp._sig = sig  # pylint: disable=protected-access
        _comp.key = key
        return _comp

    return create_component
