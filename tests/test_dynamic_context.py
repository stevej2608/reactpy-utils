
import pytest
from reactpy import component, event, use_context, use_state, html
from reactpy.testing import DisplayFixture

from reactpy_utils import DynamicContextModel, create_dynamic_context, EventArgs



@pytest.mark.anyio
async def test_local_storage(display: DisplayFixture):

    class AppState(DynamicContextModel):
        dark_mode: bool = True

    AppContext = create_dynamic_context(AppState)


    @component
    def Child():
        context, set_context = use_context(AppContext)

        @event
        def on_click(event:EventArgs):
            set_context(context.update(dark_mode = not context.dark_mode))

        return html.button({'id': 'toggle_btn', 'on_click': on_click}, f"dark_mode={context.dark_mode}")


    @component
    def TestApp():
        state, set_state = use_state(AppState())

        return AppContext(
            Child(),
            value = (state, set_state)
        )

    await display.show(TestApp)

    btn = display.page.locator('id=toggle_btn')

    text = await btn.all_inner_texts()
    assert text == ['dark_mode=True']

    await btn.click()

    text = await btn.all_inner_texts()
    assert text == ['dark_mode=False']

    assert True
