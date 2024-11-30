import pytest
from reactpy.testing import DisplayFixture

from docs.examples.python.clipboard import BUTTON_ID, TEXT, App


@pytest.mark.anyio
async def test_docs_example_copy_to_clipboard(display: DisplayFixture):
    """Just confirm that the docs example builds & runs"""
    await display.show(App)

    btn = display.page.locator(f"id={BUTTON_ID}")
    await btn.click()

    text = await display.page.evaluate("() => navigator.clipboard.readText()")
    assert text == TEXT
