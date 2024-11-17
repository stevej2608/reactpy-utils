
import pytest
from reactpy import component, event, html, use_state
from reactpy.testing import DisplayFixture

from reactpy_utils import EventArgs, DocumentTitle
from .tooling import get_document_title, page_stable


@pytest.mark.anyio
async def test_document_title(display: DisplayFixture):


    @component
    def TestApp():
        title, set_title = use_state("Hello Earth")

        @event
        def on_click(event:EventArgs):
            t = "Hello Earth" if title != "Hello Earth" else "Hello Mars"
            set_title(t)

        return html._(
            DocumentTitle(title),
            html.button({'id': "toggle_btn", 'on_click': on_click }, "Toggle Document Title")
        )

    await display.show(TestApp)
    await page_stable(display.page)

    # Confirm the initial title

    title = await get_document_title(display.page)
    assert title == "Hello Earth"

    # Toggle the title

    await display.page.locator('id=toggle_btn').click()
    await page_stable(display.page)

    # Confirm the new title

    title = await get_document_title(display.page)
    assert title == "Hello Mars"
