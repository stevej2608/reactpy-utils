from reactpy import component, event, html, use_context, use_state
from reactpy_utils import EventArgs

from .app_context import AppState, AppContext

@component
def App():
    app_state, set_app_state = use_state(AppState())
    return AppContext(
        NavBar(),
        Content(),
        value=(app_state, set_app_state),
    )

@component
def Content():
    app_state, _ = use_context(AppContext)
    return html.div(
        html.h2(f"dark_mode={app_state.dark_mode}"),
    )

@component
def NavBar():
    return html.div(
        DarkModeButton()
    )

@component
def DarkModeButton():
    app_state, set_app_state = use_context(AppContext)

    @event
    def on_click(_evt: EventArgs):
        set_app_state(app_state.update(dark_mode=not app_state.dark_mode))

    return html.button({"on_click": on_click}, "Toggle Dark Mode")
