from typing import cast, Callable, TypeVar, Type
from pydantic import BaseModel
from reactpy import create_context as reactpy_create_context

DataModel = TypeVar('DataModel', bound='DynamicContextModel')

class DynamicContextModel(BaseModel):
    """Base component for dynamic context models"""

    def update(self: DataModel , **kwargs) -> DataModel:
        model = self.model_copy(update=kwargs)
        return model

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
        theme, set_theme = use_context(AppContext)

        def on_click(event: EventArgs):
            set_theme(theme.update(theme=theme_color.value))

        return Button(f"Set {theme_color.value} theme", on_click=on_click, color=theme_color)

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
    return reactpy_create_context(cast(tuple[DataModel, Callable[[DataModel], None]], None))
