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
