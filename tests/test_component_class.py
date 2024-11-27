import pytest
import copy
from reactpy import component, html, use_state, event
from pydantic import BaseModel
from reactpy.core.types import VdomDict
from reactpy.testing import DisplayFixture

from reactpy_utils import EventArgs, class_component

from .tooling import page_stable


class TableState(BaseModel):
    row_start: int = 0
    rows: list[str] = []


@class_component
class UsersTable:

    @property
    def rows(self) -> list[str]:
        return self._table.rows

    @property
    def row_start(self) -> int:
        return self._table.row_start

    def __init__(self, table_state: TableState):
        super().__init__()
        self._table, self._set_table = use_state(table_state)

    def page_next(self) -> None:

        def update(table: TableState) -> TableState:
            table = copy.copy(table)
            table.row_start = min(table.row_start + 10, len(table.rows))
            return table

        self._set_table(update)

    @component
    def TableHeader(self):
        return html.header(html.th("User ID"))

    @component
    def TableBody(self):
        table = self._table
        first = table.row_start
        last = min(first + 10, len(table.rows))
        rows = [html.tr(html.td(row)) for row in table.rows[first:last]]
        return html.tbody(*rows)

    def render(self) -> VdomDict:
        return html.table(self.TableHeader(), self.TableBody())


@component
def PaginatorUI(table: UsersTable):

    @event
    def on_click(_evt: EventArgs):
        table.page_next()

    return html.button({"id": "next-page", "on_click": on_click}, "Next Page")


@component
def PageHeader(user_table: UsersTable):
    return html.div(
        html.h2(f"Page Header: table start = {user_table.row_start}"),
        PaginatorUI(user_table),
    )


@component
def PageContent(user_table: UsersTable):
    return html._(html.h2("Table Content"), user_table)


@component
def PageFooter(user_table: UsersTable):
    return html.h2(f"Footer: table size = {len(user_table.rows)}")


@component
def App():
    table = UsersTable(TableState(rows=[f"user-{i}" for i in range(50)]))
    return html.div(PageHeader(table), PageContent(table), PageFooter(table))


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
