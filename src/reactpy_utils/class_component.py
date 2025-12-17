from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, Callable, TypeVar, cast

from reactpy.core.component import Component
from reactpy.types import ComponentType

if TYPE_CHECKING:
    from reactpy.types import VdomDict

NONE = cast(Any, None)


class _ComponentClass(Component):
    """Base class for all ComponentClass implementations"""

    _initialized: bool = False

    def __init__(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]):
        # Store initialization args for later use
        self._init_args = args
        self._init_kwargs = kwargs

        # Create a wrapper that calls user __init__ on first render
        def _render_with_init():
            if not self._initialized:
                self._initialized = True
                # Call user's __init__ within render context
                self._user_init(*self._init_args, **self._init_kwargs)
            return self.render()

        super().__init__(function=_render_with_init, key=NONE, args=args, kwargs=kwargs, sig=NONE)

    def _user_init(self, *args: Any, **kwargs: Any) -> None:
        """User's __init__ logic - to be overridden"""
        pass

    def render(self) -> VdomDict:
        raise NotImplementedError


ClassComponent = TypeVar("ClassComponent", bound=object)


def class_component(comp: type[ClassComponent]) -> type[ClassComponent]:
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

    # Store the original __init__
    original_init = comp.__init__ if hasattr(comp, '__init__') else None

    # Create _user_init method that calls the original __init__
    def _user_init(self, *args: Any, **kwargs: Any) -> None:
        if original_init is not None:
            original_init(self, *args, **kwargs)

    # Create new class with modified initialization
    new_class_dict = {'_user_init': _user_init}
    comp = type(comp.__name__, (comp, _ComponentClass), new_class_dict)  # type: ignore
    sig = inspect.signature(comp)

    def create_component(*args: Any, key: Any | None = None, **kwargs: Any):
        # Create instance using __new__ to avoid calling __init__ yet
        _comp = comp.__new__(comp)
        # Call our custom __init__ which defers user initialization
        _ComponentClass.__init__(_comp, *args, **kwargs)

        _comp = cast(_ComponentClass, _comp)
        _comp._sig = sig  # pylint: disable=protected-access
        _comp.key = key

        _comp._args = args
        _comp._kwargs = kwargs

        _comp.type = cast(Callable[..., ComponentType], comp)

        return _comp

    return create_component  # type: ignore
