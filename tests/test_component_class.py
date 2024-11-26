import pytest
from reactpy import component, html
from reactpy.core.types import VdomDict
from reactpy.testing import DisplayFixture

from reactpy_utils.component_class import class_component


@class_component
class UsersTable:
    def __init__(self, table):
        super().__init__()
        self.table = table

    def render(self) -> VdomDict:
        return html.h2({"id": "table_row"}, f"Hello {self.table[0]}")


@pytest.mark.anyio
async def test_component_class_new(display: DisplayFixture):
    @component
    def TestApp():
        table = UsersTable(["Steve"])
        return html._(html.h2("Table Test"), table)

    await display.show(TestApp)

    text = await display.page.locator("id=table_row").all_inner_texts()
    assert text == ["Hello Steve"]

    assert True
