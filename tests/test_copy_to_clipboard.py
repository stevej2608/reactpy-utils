
import logging
import pytest
import lorem
from reactpy import component, html
from reactpy.testing import DisplayFixture

from reactpy_utils import CopyToClipboard

log = logging.getLogger(__name__)



@pytest.mark.anyio
async def test_copy_to_clipboard(display: DisplayFixture):

    BUTTON_ID = "copy-btn"
    TEXT = lorem.paragraph()

    @component
    def TestApp():
        return html._(
            html.button({'id': BUTTON_ID}, "Copy to Clipboard"),
            CopyToClipboard(button_id=BUTTON_ID, text=TEXT)
        )

    await display.show(TestApp)

    btn = display.page.locator(f'id={BUTTON_ID}')
    await btn.click()

    text = await display.page.evaluate("() => navigator.clipboard.readText()")

    assert text == TEXT
