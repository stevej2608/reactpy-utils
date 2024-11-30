from __future__ import annotations

from typing import TYPE_CHECKING, cast, Union

import pytest
from pydantic import BaseModel
from reactpy import component, html
from reactpy_router import browser_router, route

from reactpy_utils import use_params, use_search_params

if TYPE_CHECKING:
    from reactpy.testing import DisplayFixture


@pytest.mark.anyio
async def test_use_params(display: DisplayFixture):
    class MyParams(BaseModel):
        first: int = cast(int, None)
        second: int = cast(int, None)
        third: int = cast(int, None)

    expected_params: MyParams = cast(MyParams, None)

    @component
    def check_params():
        assert use_params(MyParams) == expected_params
        return html.h1({"id": "success"}, "success")

    @component
    def sample():
        return browser_router(
            route(
                "/first/{first:str}",
                check_params(),
                route(
                    "/second/{second:str}",
                    check_params(),
                    route(
                        "/third/{third:str}",
                        check_params(),
                    ),
                ),
            )
        )

    await display.show(sample)

    for path, _expected_params in [
        ("/first/1", {"first": 1}),
        ("/first/1/second/2", {"first": 1, "second": 2}),
        ("/first/1/second/2/third/3", {"first": 1, "second": 2, "third": 3}),
    ]:
        expected_params = MyParams(**_expected_params)
        await display.goto(path)
        await display.page.wait_for_selector("#success")


@pytest.mark.anyio
async def test_search_params(display: DisplayFixture):
    class MyParams(BaseModel):
        hello: Union[str, None] = None
        thing: Union[list[int], None] = None

    expected_query: MyParams = MyParams()

    @component
    def check_query():
        assert use_search_params(MyParams) == expected_query
        return html.h1({"id": "success"}, "success")

    @component
    def sample():
        return browser_router(route("/", check_query()))

    await display.show(sample)

    expected_query = MyParams(hello="world", thing=[1, 2])
    await display.goto("?hello=world&thing=1&thing=2")
    await display.page.wait_for_selector("#success")
