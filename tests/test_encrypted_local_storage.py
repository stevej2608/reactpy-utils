from typing import Self
import json
import base64
import pytest
from cryptography.fernet import Fernet
from reactpy import component, html, use_context, use_state
from reactpy.testing import DisplayFixture

from reactpy_utils import DynamicContextModel, create_dynamic_context, LocalStorageProvider

from .tooling import page_stable, read_local_storage

# KEY = Fernet.generate_key()

KEY = b'3qgHqyfztBTIDpPc1AFYt9vPXQ1Ni5lF4vwfhaMzWBs='

fernet = Fernet(KEY)

def decode(data:str) -> str:
    """Decode encrypted json data to a stringified json object"""
    encMessage = base64.b64decode(data)
    plane = fernet.decrypt(encMessage).decode()
    return json.dumps(json.loads(plane))


def encode(plain_text:str) -> str:
    """Encode the plain_text stringified json object to an encrypted, base64, stringified json object"""
    encMessage = fernet.encrypt(plain_text.encode())
    encMessage64 = base64.b64encode(encMessage).decode('utf-8')
    return json.dumps({"data": encMessage64})


class CurrentUserState(DynamicContextModel):
    user_name :str
    password : str

    def update(self: Self, **kwargs) -> Self:
        """Return a new model instance based on the current model with the field changes defined in **kwargs"""
        plane = decode(**kwargs)
        kwargs = json.loads(plane)
        model = super().update(**kwargs)
        return model


    def dumps(self, sort_keys=True) -> str:
        """Convert model to an encrypted json string"""
        plane_text = super().dumps(sort_keys=sort_keys)
        return encode(plane_text)



AppContext = create_dynamic_context(CurrentUserState)

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
    assert local_storage == '{"password": "123", "user_name": "steve"}'

    assert True
