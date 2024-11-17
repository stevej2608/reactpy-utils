from reactpy import component, event, html, use_state, use_context, run

from reactpy_utils import EventArgs, DynamicContextModel, create_dynamic_context, LocalStorageAgent, When

class AppState(DynamicContextModel):
    dark_mode: bool = True

AppContext = create_dynamic_context(AppState)

@component
def MyApp():
    app_state, set_app_state = use_context(AppContext)

    @event
    def on_click(event:EventArgs):
        set_app_state(app_state.update(dark_mode = not app_state.dark_mode))

    return html.div(
        html.h2({'id': "h2"}, f"dark_mode={app_state.dark_mode}"),
        html.button({'id': "toggle_btn", 'on_click': on_click }, "Toggle Dark Mode"),

    )


@component
def AppMain():
    app_state, set_app_state = use_state(AppState())

    return AppContext(
        html._(
            When(app_state.is_valid, MyApp()),
            LocalStorageAgent(ctx=AppContext, storage_key="local-storage-test"),
        ),
        value = (app_state, set_app_state)
    )

# python -m examples.local_storage_example

if __name__ == "__main__":
    run(AppMain)
