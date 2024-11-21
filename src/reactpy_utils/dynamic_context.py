from __future__ import annotations

import json
from typing import TYPE_CHECKING, Callable, Protocol, Self, TypeVar, cast

from pydantic import BaseModel
from reactpy import create_context as reactpy_create_context

if TYPE_CHECKING:
    from reactpy.types import Context


DataModel = TypeVar("DataModel", bound="DynamicContextModel")


class DynamicContextModel(BaseModel):
    """Base component for dynamic context models"""

    _update_count: int = 0

    @property
    def is_valid(self):
        """Return True if the context values have been updated. A False value indicates that the
        values are the default values"""

        return self._update_count > 0

    def update(self: Self, **kwargs) -> Self:
        """Return a new model instance based on the current model with the field changes defined in **kwargs"""
        values = {**self.model_dump(), **kwargs}
        model = type(self)(**values)
        model._update_count = self._update_count + 1  # pylint: disable=protected-access
        return model

    def dumps(self, sort_keys=True) -> str:
        """Convert model to json string"""
        return json.dumps(self.model_dump(), sort_keys=sort_keys)

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}, {self.__str__()}"

    def __str__(self):
        return json.dumps({"is_valid": self.is_valid, "state": self.model_dump()}, sort_keys=True)


class IDynamicContextModel(Protocol):
    """Define protocol to allow DynamicContextModel to be duck typed"""

    @property
    def is_valid(self):
        """Return True if the context values have been updated. A False value indicates that the
        values are the default values"""

    def dumps(self, sort_keys=True) -> str:  # type: ignore
        """Convert model to json string"""

    def update(self: Self, **kwargs) -> Self:  # type: ignore
        """Return a new model instance based on the current model with the field changes defined in **kwargs"""


class CustomDynamicContextModel(IDynamicContextModel):
    """Alternative, non-pydantic, base class from which to sub-class context models"""

    def __init__(self):
        self._update_count = 0

    @property
    def is_valid(self) -> bool: # type: ignore
        return self._update_count > 0

    def dumps(self, sort_keys=True) -> str:
        values = self.__dict__.copy()
        values.pop("_update_count")
        return json.dumps(values, sort_keys=sort_keys)

    def update(self: Self, **kwargs) -> Self:
        values = json.loads(self.dumps())
        model = type(self)(**{**values, **kwargs})
        model._update_count = self._update_count + 1  # pylint: disable=protected-access
        return model


_Type = TypeVar("_Type", bound=DynamicContextModel | IDynamicContextModel)
_ReturnType = tuple[_Type, Callable[[_Type | Callable[[_Type], _Type]], None]]


def create_dynamic_context(_model: type[_Type]) -> Context[_ReturnType[_Type]]:
    """Create a context that is settable from child components

    Usage:
    ```
    from reactpy_utils.dynamic_context import (
        create_dynamic_context,
        DynamicContextModel,
    )


    class AppState(DynamicContextModel):
        theme: str = "Red"
        ...


    AppContext = create_dynamic_context(AppState)


    @component
    def ThemeButton(theme_color: ButtonColor):
        context, set_context = use_context(AppContext)

        def on_click(event: EventArgs):
            set_context(lambda ctx: ctx.update(theme=theme_color))

        return Button(
            f"Set {theme_color} theme", on_click=on_click, color=theme_color
        )


    @component
    def Layout():
        state, set_state = use_state(AppState())
        return AppContext(html._(...), value=(state, set_state))
    ```
    """

    return reactpy_create_context(cast(_ReturnType[_Type], None))
