from __future__ import annotations

from reactpy import component, html

from reactpy_utils import props

# pylint: disable=unused-argument, no-member, line-too-long


def test_simple():
    @component
    def Include(
        label: str | None = None,
        id: str | None = None,
        name: str | None = None,
        placeholder: str | None = None,
        value: str | None = None,
    ):
        _props = props(include="id, name, placeholder, value")
        return html.input(_props)

    @component
    def Exclude(
        label: str | None = None,
        id: str | None = None,
        name: str | None = None,
        placeholder: str | None = None,
        value: str | None = None,
    ):
        _props = props(exclude="placeholder, value")
        return html.input(_props)

    result = Include(id="search", name="search", placeholder="Search", label="Search", value="").render()
    assert result["attributes"] == {"id": "search", "name": "search", "placeholder": "Search", "value": ""}  # type: ignore

    result = Exclude(id="search", name="search", placeholder="Search", label="Search", value="").render()
    assert result["attributes"] == {"label": "Search", "id": "search", "name": "search"}  # type: ignore
