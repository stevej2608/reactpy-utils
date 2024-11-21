import pytest
from reactpy import component, event, html, use_state
from reactpy.testing import DisplayFixture

from docs.examples.python.local_storage import App
from reactpy_utils import DynamicContextModel, EventArgs, LocalStorageAgent, create_dynamic_context

from .tooling import page_stable, read_local_storage


class AppState(DynamicContextModel):
    dark_mode: bool = True


AppContext = create_dynamic_context(AppState)


@pytest.mark.anyio
async def test_local_storage(display: DisplayFixture):
    """Test the the AppContext is synchronized with the browser local
    storage and that the context is re-loaded from local storage on a
    page reload."""

    render_count = 0

    @component
    def TestApp():
        nonlocal render_count
        app_state, set_app_state = use_state(AppState())

        @event
        def on_click(_evt: EventArgs):
            set_app_state(app_state.update(dark_mode=not app_state.dark_mode))

        render_count += 1

        return AppContext(
            html._(
                html.h2({"id": "h2"}, f"dark_mode={app_state.dark_mode}"),
                html.button({"id": "toggle_btn", "on_click": on_click}, "Toggle Dark Mode"),
                LocalStorageAgent(ctx=AppContext, storage_key="local-storage-test"),
            ),
            value=(app_state, set_app_state),
        )

    await display.show(TestApp)

    # Confirm the dark_mode has been rendered by the h2 element to the default value

    text = await display.page.locator("id=h2").all_inner_texts()
    assert text == ["dark_mode=True"]

    # Confirm we have the initial render and a second render due to
    # local storage synchronization of the context

    assert render_count == 2

    # Confirm, via playwright, that the default value is in local storage

    local_storage = await read_local_storage(display.page, "local-storage-test")
    assert local_storage == '{"dark_mode": true}'

    # Toggle the dark mode button

    await display.page.locator("id=toggle_btn").click()
    await page_stable(display.page)

    # Confirm additional render after button click

    assert render_count == 3

    # Confirm dark_mode has been toggled in the h2 element (to False)

    text = await display.page.locator("id=h2").all_inner_texts()
    assert text == ["dark_mode=False"]

    # Confirm dark_mode in local storage has been toggled (to False)

    local_storage = await read_local_storage(display.page, "local-storage-test")
    assert local_storage == '{"dark_mode": false}'

    # Force a page reload

    await display.page.reload()
    await page_stable(display.page)

    # Confirm the reload has force a re-render and a second render due to
    # local storage synchronization of the context

    assert render_count == 5

    # Confirm the dark_mode of the h2 element has taken the saved
    # value from localStorage (False)

    text = await display.page.locator("id=h2").all_inner_texts()
    assert text == ["dark_mode=False"]


@pytest.mark.anyio
async def test_example(display: DisplayFixture):
    await display.show(App)

    local_storage = await read_local_storage(display.page, "local-storage-example")
    assert local_storage == '{"dark_mode": true}'
