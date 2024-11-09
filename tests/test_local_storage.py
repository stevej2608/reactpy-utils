
import logging
import pytest
from reactpy import component, event, html, use_state
from reactpy.testing import DisplayFixture

from reactpy_utils import EventArgs, DynamicContextModel, create_dynamic_context, LocalStorageAgent
from .tooling import wait_page_stable, read_local_storage

log = logging.getLogger(__name__)

class AppState(DynamicContextModel):
    dark_mode: bool = True

AppContext = create_dynamic_context(AppState)

@pytest.mark.anyio
async def test_local_storage(display: DisplayFixture):
    render_count = 0

    @component
    def TestApp():
        nonlocal render_count
        app_state, set_app_state = use_state(AppState())

        # log.info('********** TestApp app_state=%s ****************', app_state)

        @event
        def on_click(event:EventArgs):
            set_app_state(app_state.update(dark_mode = not app_state.dark_mode))

        render_count += 1

        return AppContext(
            html._(
                html.h2({'id': "h2"}, f"dark_mode={app_state.dark_mode}"),
                html.button({'id': "toggle_btn", 'on_click': on_click }, "Toggle Dark Mode"),
                LocalStorageAgent(ctx=AppContext, storage_key="local-storage-test"),
            ),
            value = (app_state, set_app_state)
        )

    await display.show(TestApp)

    # Confirm the dark_mode has been rendered by the h2 element

    text = await display.page.locator('id=h2').all_inner_texts()
    assert text == ['dark_mode=True']

    # Confirm the value is in local storage

    local_storage = await read_local_storage(display.page, "local-storage-test")
    assert local_storage == '{"dark_mode": true}'

    await display.page.locator('id=toggle_btn').click()

    # Confirm dark_mode has been toggled in the h2 element (to False)

    text = await display.page.locator('id=h2').all_inner_texts()
    assert text == ['dark_mode=False']

    # Confirm dark_mode in local storage has been toggled (to False)

    local_storage = await read_local_storage(display.page, "local-storage-test")
    assert local_storage == '{"dark_mode": false}'

    assert render_count == 2

    # log.info('********** PAGE REALOD ****************')

    await display.page.reload()
    await wait_page_stable(display.page)

    # Confirm the dark_mode has been the h2 element has taken the saved
    # value from localStorage (False)

    text = await display.page.locator('id=h2').all_inner_texts()
    assert text == ['dark_mode=False']

    assert render_count == 4
