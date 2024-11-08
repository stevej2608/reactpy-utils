
import pytest
from reactpy import component, html
from reactpy.testing import DisplayFixture, poll
from reactpy.utils import Ref
from tests.tooling.hooks import use_toggle

# https://github.com/reactive-python/reactpy/blob/reactpy-v1.0.2/src/py/reactpy/tests/test_html.py

@pytest.mark.anyio
async def test_script_mount_unmount(display: DisplayFixture):
    toggle_is_mounted = Ref()

    @component
    def Root():
        is_mounted, toggle_is_mounted.current = use_toggle(True)
        return html.div(
            html.div({"id": "mount-state", "data_value": False}),
            HasScript() if is_mounted else html.div(),
        )

    @component
    def HasScript():
        return html.script(
            """() => {
                const mapping = {"false": false, "true": true};
                const mountStateEl = document.getElementById("mount-state");

                mountStateEl.setAttribute(
                    "data-value", !mapping[mountStateEl.getAttribute("data-value")]);

                // Return a teardown that is called when the script element 
                // is removed from the tree, or when the script content changes.

                return () => mountStateEl.setAttribute(
                    "data-value", !mapping[mountStateEl.getAttribute("data-value")]);
            }"""
        )

    # Display the test component

    await display.show(Root)

    mount_state = await display.page.wait_for_selector("#mount-state", state="attached")

    # The loaded state of #mount-state 'data_value' attribute is False. The script is
    # injected and when it runs it toggles 'data_value'. Confirm the value has been
    # toggled.

    poll_mount_state = poll(mount_state.get_attribute, "data-value")
    await poll_mount_state.until_equals("true")

    # Toggle the is_mounted state variable. This will result in the html.script
    # element being removed from the DOM tree. The removal will trigger the teardown
    # function which will toggle 'data_value'. Confirm the value has been
    # toggled.

    toggle_is_mounted.current()
    await poll_mount_state.until_equals("false")

    # Toggle the is_mounted state variable. The script is
    # injected and when it runs it toggles 'data_value'. Confirm the value has been
    # toggled again

    toggle_is_mounted.current()
    await poll_mount_state.until_equals("true")
