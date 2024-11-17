## reactpy-utils

Collection of reactpy helpers. 

    pip install reactpy-utils

### Components

The following components are available:

**DocumentTitle** Update the Browser Tab by setting the DOM *document.title*

```python
from reactpy import component, event, html, use_state
from reactpy_utils import EventArgs, DocumentTitle

@component
def TestApp():
    title, set_title = use_state("Hello Earth")

    @event
    def on_click(event:EventArgs):
        t = "Hello Earth" if title != "Hello Earth" else "Hello Mars"
        set_title(t)

    return html._(
        DocumentTitle(title),
        html.button({'on_click': on_click }, "Toggle Document Title")
    )

```
**CopyToClipboard** Copy text to the browser clipboard.

```python
import lorem
from reactpy import component, html
from reactpy_utils import CopyToClipboard


BUTTON_ID = "copy-btn"
TEXT = lorem.paragraph()

@component
def TestApp():
    return html._(
        html.button({'id': BUTTON_ID}, "Copy to Clipboard"),
        CopyToClipboard(button_id=BUTTON_ID, text=TEXT)
    )

```

**LocalStorageAgent** Save and restore to browser local storage. Context is restores on page reload.

```python
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
        html.h2(f"dark_mode={app_state.dark_mode}"),
        html.button({'on_click': on_click }, "Toggle Dark Mode"),
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
```
