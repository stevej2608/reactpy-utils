
import lorem
import pytest
from reactpy import component, html
from reactpy.testing import DisplayFixture

from reactpy_utils import CopyToClipboard

from docs.examples.clipboard import App, TEXT

from .tooling import page_stable


@pytest.mark.anyio
async def test_copy_to_clipboard(display: DisplayFixture):
    _BUTTON_ID = "copy-btn"
    _TEXT = lorem.paragraph()

    @component
    def TestApp():
        return html._(
            html.button({"id": _BUTTON_ID}, "Copy to Clipboard"), CopyToClipboard(button_id=_BUTTON_ID, text=_TEXT)
        )

    await display.show(TestApp)

    btn = display.page.locator(f"id={_BUTTON_ID}")
    await btn.click()

    text = await display.page.evaluate("() => navigator.clipboard.readText()")
    assert text == _TEXT


@pytest.mark.anyio
async def test_example(display: DisplayFixture):
    await display.show(App)
    await page_stable(display.page)
    text = await display.page.evaluate("() => navigator.clipboard.readText()")
    assert text == TEXT
