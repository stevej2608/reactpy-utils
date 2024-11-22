import pytest
from reactpy.testing import DisplayFixture

from docs.examples.python.clipboard import BUTTON_ID, TEXT, App


@pytest.mark.anyio
async def test_example(display: DisplayFixture):
    """Just confirm that the docs example builds & runs"""
    await display.show(App)

    btn = display.page.locator(f"id={BUTTON_ID}")
    await btn.click()

    text = await display.page.evaluate("() => navigator.clipboard.readText()")
    assert text == TEXT
