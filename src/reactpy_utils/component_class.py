from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, TypeVar, cast

from reactpy.core.component import Component

if TYPE_CHECKING:
    from reactpy.core.types import ComponentType, VdomDict

NONE = cast(Any, None)


class ComponentClass(Component):
    def __init__(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]):
        super().__init__(function=self.render, key=NONE, args=args, kwargs=kwargs, sig=NONE)

    def render(self) -> VdomDict:
        raise NotImplementedError


ClassComponent = TypeVar("ClassComponent", bound=ComponentClass)


def class_component(comp: type[ClassComponent]):
    """ReactPy ComponentClass decorator

    Args:
        comp (ComponentClass): Class to be wrapped

    Usage:
    ```
        from reactpy import html, run
        from utils.component_class import class_component, ComponentClass

        @class_component
        class HelloWorld(ComponentClass):

            def render(self):
                return html.h2('Hello World!')

        run(HelloWorld)
    ```
    """

    sig = inspect.signature(comp)

    def create_component(*args: Any, key: Any | None = None, **kwargs: Any) -> ComponentType:
        _comp = comp(*args, **kwargs)
        _comp._sig = sig  # pylint: disable=protected-access
        _comp.key = key
        return _comp

    return create_component
