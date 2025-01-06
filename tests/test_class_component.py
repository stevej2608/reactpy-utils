import pytest
from reactpy import html
from reactpy.core.types import VdomDict
from reactpy.testing import DisplayFixture

from docs.examples.python.class_component import App
from reactpy_utils import class_component

from .tooling import page_stable


def test_render_missing(display: DisplayFixture):

    @class_component
    class RenderMissing:
        """Class must have a render() method"""

        def __init__(self):
            super().__init__()

    try:
        component = RenderMissing()
        component.render()  # type: ignore
    except NotImplementedError:
        assert True

def test_str(display: DisplayFixture):

    @class_component
    class TitleComponent:

        def __init__(self, title:str):
            super().__init__()
            self.title = title

        def render(self) -> VdomDict:
            return html.h2(self.title)

    component = TitleComponent(title="Main Page")
    assert f"{component}" == f"TitleComponent({id(component):02x}, title='Main Page')"



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
