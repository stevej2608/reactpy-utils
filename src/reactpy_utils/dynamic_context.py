from __future__ import annotations
import json
from typing import TypeVar, cast, Callable, Type
from pydantic import BaseModel
from reactpy import create_context as reactpy_create_context

DataModel = TypeVar('DataModel', bound='DynamicContextModel')

DataModelSetter = Callable[[DataModel | Callable[[DataModel], DataModel]], None]

IDataModel = tuple[DataModel, DataModelSetter]

class DynamicContextModel(BaseModel):
    """Base component for dynamic context models"""

    _update_count: int = 0

    @property
    def is_valid(self):
        """Return True if the context values have been updated. A False value indicates that the 
        values are the default values"""

        return self._update_count > 0

    def update(self: DataModel , **kwargs) -> DataModel:
        """Return a new model instance based on the current model with the field changes defined in **kwargs"""
        values = {**self.model_dump(), **kwargs}
        model = type(self)(**values)
        model._update_count = self._update_count + 1
        return model
    
    def dumps(self, sort_keys=True):
        return json.dumps(self.model_dump(), sort_keys=sort_keys)
    
    def __str__(self):
        return self.dumps()


def create_dynamic_context(model: Type[DataModel]):
    """Create a context that is settable from child components

    Usage:
    ```
    from reactpy_utils.dynamic_context import create_dynamic_context, DynamicContextModel

    class AppState(DynamicContextModel):
        theme: str = 'Red'
        ...

    AppContext = create_dynamic_context(AppState)


    @component
    def ThemeButton(theme_color: ButtonColor):
        context, set_context = use_context(AppContext)

        def on_click(event: EventArgs):
            set_context(lambda ctx: ctx.update(theme=theme_color))

        return Button(f"Set {theme_color} theme", on_click=on_click, color=theme_color)

    @component
    def Layout():
        state, set_state = use_state(AppState())
        return AppContext(
                html._(
                    ...
                ),
                value=(state, set_state)
            )

    ```
    """

    context = reactpy_create_context(cast(IDataModel, None))
    return context
