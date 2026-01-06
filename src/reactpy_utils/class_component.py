from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, Callable, TypeVar, cast

from reactpy.core.component import Component

if TYPE_CHECKING:
    from reactpy.types import VdomDict

NONE = cast(Any, None)


class _ComponentClass(Component):
    """Base class for all ComponentClass implementations"""

    _initialized: bool = False
    _in_user_init: bool = False

    def __init__(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]):
        # If we're already in user_init, this is a recursive call from super().__init__()
        # Just return without doing anything
        if self._in_user_init:
            return

        # Create a wrapper that calls the user's render method
        def _render_wrapper(*_args, **_kwargs):
            # Ignore the args/kwargs passed here - they're already bound to the instance
            return self._user_render()

        # Get the signature of the wrapped class for proper argument binding
        sig = inspect.signature(self.__class__)

        # V2 Component.__init__ uses positional arguments: (function, key, args, kwargs, sig)
        super().__init__(_render_wrapper, None, args, kwargs, sig)

        # Now call the user's __init__ with the flag set
        self._in_user_init = True
        self._user_init(*args, **kwargs)
        self._in_user_init = False

    def _user_init(self, *args: Any, **kwargs: Any) -> None:
        """User's __init__ logic - to be overridden"""
        pass

    def _user_render(self) -> VdomDict:
        """User's render logic - to be overridden"""
        raise NotImplementedError

    def __repr__(self) -> str:
        """Override repr to show the actual class name instead of _render_wrapper"""
        try:
            args = self._sig.bind(*self._args, **self._kwargs).arguments
        except TypeError:
            return f"{self.__class__.__name__}(...)"
        else:
            items = ", ".join(f"{k}={v!r}" for k, v in args.items())
            if items:
                return f"{self.__class__.__name__}({id(self):02x}, {items})"
            else:
                return f"{self.__class__.__name__}({id(self):02x})"


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

    # Store the original __init__ and render methods
    original_init = comp.__init__ if hasattr(comp, '__init__') else None
    original_render = comp.render if hasattr(comp, 'render') else None

    # Store the original signature BEFORE wrapping
    original_sig = inspect.signature(comp)

    # Create _user_init method that calls the original __init__
    def _user_init(self, *args: Any, **kwargs: Any) -> None:
        if original_init is not None:
            original_init(self, *args, **kwargs)

    # Create _user_render method that calls the original render
    def _user_render(self) -> VdomDict:
        if original_render is None:
            raise NotImplementedError(f"{comp.__name__} must implement a render() method")
        return original_render(self)

    # Create new class with modified initialization and render
    new_class_dict = {'_user_init': _user_init, '_user_render': _user_render}
    comp = type(comp.__name__, (comp, _ComponentClass), new_class_dict)  # type: ignore
    # Use the original signature, not the wrapped one
    sig = original_sig

    def create_component(*args: Any, key: Any | None = None, **kwargs: Any):
        # Create instance using __new__ to avoid calling __init__ yet
        _comp = comp.__new__(comp)
        # Call our custom __init__ which defers user initialization
        _ComponentClass.__init__(_comp, *args, **kwargs)

        _comp = cast(_ComponentClass, _comp)
        # Component.__init__ already sets these, but we may need to override key
        if key is not None:
            _comp.key = key

        return _comp

    return create_component  # type: ignore
