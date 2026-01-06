import lorem
from reactpy import component, html

from reactpy_utils import CopyToClipboard

from utils.pico_run import run

BUTTON_ID = "test-copy-btn"
TEXT = lorem.paragraph()

@component
def App():
    return html._(html.button({"id": BUTTON_ID}, "Copy to Clipboard"), CopyToClipboard(button_id=BUTTON_ID, text=TEXT))

# python -m docs.examples.python.clipboard
if __name__ == "__main__":
    run(App)

