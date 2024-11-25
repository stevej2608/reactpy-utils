import pytest
from reactpy import component, html
from reactpy.core.types import VdomDict
from reactpy.testing import DisplayFixture

from reactpy_utils import ComponentClass, class_component


@class_component
class UsersTable(ComponentClass):
    def render(self) -> VdomDict:
        return html.h2("Hello World!")


@pytest.mark.anyio
async def test_copy_to_clipboard(display: DisplayFixture):
    @component
    def TestApp():
        table = UsersTable(["Steve"])

        return html._(table)

    await display.show(TestApp)

    assert True
