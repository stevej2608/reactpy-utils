import pytest
from reactpy import component, event, html, use_context, use_state
from reactpy.testing import DisplayFixture

from docs.examples.python.app_context import AppContext, AppState
from reactpy_utils.types import EventArgs

from .tooling import page_stable


@pytest.mark.anyio
async def test_dynamic_context(display: DisplayFixture):
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


@pytest.mark.anyio
async def test_nested_dynamic_context(display: DisplayFixture):
    """Confirm the same context can be instantiated at several levels in the
    component tree. A context update should only update & force a re-rendering of
    the context owner and it's child components.
    """

    test_app_render_count = 0
    child_render_count = {}
    grandchild_render_count = {}

    @component
    def GrandchildChild(id=str):
        nonlocal grandchild_render_count
        context, set_context = use_context(AppContext)

        @event
        def on_click(_evt: EventArgs):
            set_context(context.update(dark_mode=not context.dark_mode))

        my_id = f"grandchild{id}"

        if my_id not in grandchild_render_count:
            grandchild_render_count[my_id] = 1
        else:
            grandchild_render_count[my_id] += 1

        return html.div(
            html.h2(f"{my_id}: dark_mode={context.dark_mode}"),
            html.button({"id": f"grandchild_toggle_btn{id}", "on_click": on_click}, f"dark_mode={context.dark_mode}"),
        )

    @component
    def Child(id=str):
        nonlocal child_render_count
        context, set_context = use_context(AppContext)

        state, set_state = use_state(AppState())

        @event
        def on_click(_evt: EventArgs):
            set_context(context.update(dark_mode=not context.dark_mode))

        my_id = f"child{id}"

        if my_id not in child_render_count:
            child_render_count[my_id] = 1
        else:
            child_render_count[my_id] += 1

        return AppContext(
            html.h2(f"{my_id}: dark_mode={context.dark_mode}"),
            html.button({"id": f"child_toggle_btn{id}", "on_click": on_click}, f"dark_mode={context.dark_mode}"),
            *[GrandchildChild(f"{id}-{i}") for i in range(3)],
            value=(state, set_state),
        )

    @component
    def TestApp():
        nonlocal test_app_render_count
        state, set_state = use_state(AppState())

        test_app_render_count += 1

        return AppContext(*[Child(f"-{i}") for i in range(3)], value=(state, set_state))

    await display.show(TestApp)
    await page_stable(display.page)

    # Confirm everything has rendered once

    assert test_app_render_count == 1
    assert list(child_render_count.values()) == [1, 1, 1]
    assert list(grandchild_render_count.values()) == [1, 1, 1, 1, 1, 1, 1, 1, 1]

    # Click a the dark mode button in one of the children. This toggles the
    # top-level application context forcing all the children & grandchildren
    # to re-render.

    btn = display.page.locator("id=child_toggle_btn-1")
    await btn.click()
    await page_stable(display.page)

    # Confirm all children & grandchildren have re-rendered

    assert test_app_render_count == 2
    assert list(child_render_count.values()) == [2, 2, 2]
    assert list(grandchild_render_count.values()) == [2, 2, 2, 2, 2, 2, 2, 2, 2]

    # Click a the dark mode button in one of the grandchildren. This toggles the
    # associated parent context forcing all the parent & associated grandchildren
    # to re-render.

    btn = display.page.locator("id=grandchild_toggle_btn-1-1")
    await btn.click()
    await page_stable(display.page)

    # Confirm only child one and it's children  have re-rendered

    assert test_app_render_count == 2
    assert list(child_render_count.values()) == [2, 3, 2]
    assert list(grandchild_render_count.values()) == [2, 2, 2, 3, 3, 3, 2, 2, 2]

    assert True
