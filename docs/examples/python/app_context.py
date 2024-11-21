from reactpy_utils import DynamicContextModel, create_dynamic_context


class AppState(DynamicContextModel):
    dark_mode: bool = True


AppContext = create_dynamic_context(AppState)
