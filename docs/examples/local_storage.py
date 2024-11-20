from reactpy import component, html, use_state
from reactpy_utils import DynamicContextModel, LocalStorageAgent, create_dynamic_context


class AppState(DynamicContextModel):
    dark_mode: bool = True


AppContext = create_dynamic_context(AppState)


@component
def App():
    app_state, set_app_state = use_state(AppState())

    return AppContext(
        html._(
            LocalStorageAgent(ctx=AppContext, storage_key="local-storage-example"),
        ),
        value=(app_state, set_app_state),
    )
