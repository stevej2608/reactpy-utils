import pytest
from reactpy.testing import DisplayFixture

from docs.examples.python.class_component import App

from .tooling import page_stable


@pytest.mark.anyio
async def test_component_class_new(display: DisplayFixture):
    await display.show(App)
    await page_stable(display.page)

    td = display.page.locator("#app > div > table > tbody > tr:nth-child(1) > td")

    text = await td.all_inner_texts()
    assert text == ["user-0"]

    btn = display.page.locator("id=next-page")
    await btn.click()
    await page_stable(display.page)

    text = await td.all_inner_texts()
    assert text == ["user-10"]

    assert True
