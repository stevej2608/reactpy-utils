from reactpy import component, event, html, use_context, use_state

from reactpy_utils import EventArgs, LocalStorageProvider

from .app_context import AppContext, AppState


@component
def App():
    app_state, set_app_state = use_state(AppState())

    return AppContext(
        LocalStorageProvider(ExamplePage(), ctx=AppContext, storage_key="local-storage-example"),
        value=(app_state, set_app_state),
    )


@component
def ExamplePage():
    app_state, set_app_state = use_context(AppContext)

    @event
    def on_click(_evt: EventArgs):
        set_app_state(app_state.update(dark_mode=not app_state.dark_mode))

    return html.div(
        html.h2({"id": "h2"}, f"dark_mode={app_state.dark_mode}"),
        html.button({"id": "toggle_btn", "on_click": on_click}, "Toggle Dark Mode"),
    )
