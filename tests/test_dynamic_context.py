import logging

import pytest
from reactpy import component, event, html, use_context, use_state
from reactpy.testing import DisplayFixture

from reactpy_utils import DynamicContextModel, EventArgs, create_dynamic_context

log = logging.getLogger(__name__)


class AppState(DynamicContextModel):
    dark_mode: bool = True


AppContext = create_dynamic_context(AppState)


@pytest.mark.anyio
async def test_dynamic_context(display: DisplayFixture):
    test_app_render_count = 0
    child_render_count = 0

    @component
    def Child():
        nonlocal child_render_count
        context, set_context = use_context(AppContext)

        @event
        def on_click(event: EventArgs):
            set_context(context.update(dark_mode=not context.dark_mode))

        child_render_count += 1

        return html.button({"id": "toggle_btn", "on_click": on_click}, f"dark_mode={context.dark_mode}")

    @component
    def TestApp():
        nonlocal test_app_render_count
        state, set_state = use_state(AppState())

        test_app_render_count += 1

        return AppContext(Child(), value=(state, set_state))

    await display.show(TestApp)

    assert test_app_render_count == 1
    assert child_render_count == 1

    btn = display.page.locator("id=toggle_btn")
    text = await btn.all_inner_texts()
    assert text == ["dark_mode=True"]

    await btn.click()

    text = await btn.all_inner_texts()
    assert text == ["dark_mode=False"]

    assert test_app_render_count == 2
    assert child_render_count == 2
