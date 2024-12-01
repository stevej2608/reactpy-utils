import pytest
from reactpy import component, event, html, use_context, use_state
from reactpy.testing import DisplayFixture

from reactpy_utils import CustomDynamicContextModel, create_dynamic_context
from reactpy_utils.types import EventArgs

from .tooling import page_stable


class CurrentUserState(CustomDynamicContextModel):
    def __init__(self, user_name: str, password: str, dark_mode: bool = True):
        super().__init__()
        self.user_name = user_name
        self.password = password
        self.dark_mode = dark_mode


AppContext = create_dynamic_context(CurrentUserState)


@pytest.mark.anyio
async def test_custom_dynamic_context(display: DisplayFixture):
    test_app_render_count = 0
    child_render_count = 0

    @component
    def Child():
        nonlocal child_render_count
        context, set_context = use_context(AppContext)

        @event
        def on_click(_evt: EventArgs):
            set_context(context.update(dark_mode=not context.dark_mode))

        child_render_count += 1

        return html.button(
            {"id": "toggle_btn", "on_click": on_click}, f"dark_mode={context.dark_mode}, is_valid={context.is_valid}"
        )

    @component
    def TestApp():
        nonlocal test_app_render_count
        state, set_state = use_state(CurrentUserState(user_name="steve", password="123"))

        test_app_render_count += 1

        return AppContext(Child(), value=(state, set_state))

    await display.show(TestApp)
    await page_stable(display.page)

    assert test_app_render_count == 1
    assert child_render_count == 1

    btn = display.page.locator("id=toggle_btn")
    text = await btn.all_inner_texts()
    assert text == ["dark_mode=True, is_valid=False"]

    await btn.click()

    text = await btn.all_inner_texts()
    assert text == ["dark_mode=False, is_valid=True"]

    assert test_app_render_count == 2
    assert child_render_count == 2
