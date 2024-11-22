import json
import pytest
from reactpy import component, html, use_context, use_state
from reactpy.testing import DisplayFixture

from reactpy_utils import LocalStorageProvider

from docs.examples.python.encrypted_app_context import CurrentUserState, AppContext, decode

from .tooling import page_stable, read_local_storage


@component
def App():
    app_state, set_app_state = use_state(CurrentUserState(user_name="steve", password="123"))

    return AppContext(
        LocalStorageProvider(ExamplePage(), ctx=AppContext, storage_key="encrypted-local-storage-example"),
        value=(app_state, set_app_state),
    )

@component
def ExamplePage():
    app_state, _ = use_context(AppContext)

    return html.div(
        html.h2({"id": "user_name"}, f"user : {app_state.user_name}"),
        html.h2({"id": "h2"}, f"password : {app_state.password}"),
    )


@pytest.mark.anyio
async def test_example(display: DisplayFixture):
    """Confirm local storage holds encrypted value"""

    await display.show(App)
    await page_stable(display.page)

    # Read the encrypted context from local storage

    local_storage = await read_local_storage(display.page, "encrypted-local-storage-example")

    # Decrypt it and validate it

    local_storage = decode(**json.loads(local_storage))
    assert local_storage == {'password': '123', 'user_name': 'steve'}

    assert True
