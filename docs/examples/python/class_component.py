import copy
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from reactpy import component, event, html, run, use_state
from reactpy.core.types import VdomDict

from reactpy_utils import class_component
from reactpy_utils.types import EventArgs

TData = TypeVar("TData", bound=Any)


class TableState(BaseModel, Generic[TData]):
    row_start: int = 0
    rows: list[TData] = []


@class_component
class BasicTable(Generic[TData]):
    def __init__(self, rows: list[TData]):
        super().__init__()
        self._table, self._set_table = use_state(TableState(rows=rows))

    @property
    def rows(self) -> list[TData]:
        return self._table.rows

    @property
    def row_start(self) -> int:
        return self._table.row_start

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
def App():
    @component
    def PaginatorUI(table: BasicTable):
        @event
        def on_click(_evt: EventArgs):
            table.page_next()

        return html.button({"id": "next-page", "on_click": on_click}, "Next Page")

    @component
    def PageHeader(user_table: BasicTable):
        return html.div(
            html.h2(f"Page Header: table start = {user_table.row_start}"),
            PaginatorUI(user_table),
        )

    @component
    def PageContent(user_table: BasicTable):
        return html._(html.h2("Table Content"), user_table)

    @component
    def PageFooter(user_table: BasicTable):
        return html.h2(f"Footer: table size = {len(user_table.rows)}")

    table = BasicTable(rows=[f"user-{i}" for i in range(50)])
    return html.div(PageHeader(table), PageContent(table), PageFooter(table))


# python -m docs.examples.python.class_component

if __name__ == "__main__":
    run(App)
