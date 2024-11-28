import lorem
from reactpy import component, html

from reactpy_utils import CopyToClipboard

BUTTON_ID = "test-copy-btn"
TEXT = lorem.paragraph()


@component
def App():
    return html._(
        html.button({"id": BUTTON_ID}, "Copy to Clipboard"), 
        CopyToClipboard(button_id=BUTTON_ID, text=TEXT)
    )
