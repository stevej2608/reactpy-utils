import base64
import json

from cryptography.fernet import Fernet
from typing_extensions import Self

from reactpy_utils import DynamicContextModel, create_dynamic_context

# Use Fernet.generate_key() to create keys. The key remains on
# the server, only encrypted data is sent to the browser.

fernet = Fernet(b"3qgHqyfztBTIDpPc1AFYt9vPXQ1Ni5lF4vwfhaMzWBs=")


def decode(data: str) -> dict:
    """Decode encrypted json data to a json object"""
    encMessage = base64.b64decode(data)
    plane = fernet.decrypt(encMessage).decode()
    return json.loads(plane)


def encode(plain_text: str) -> str:
    """Encode the plain_text stringified json object to an encrypted, base64, stringified json object"""
    encMessage = fernet.encrypt(plain_text.encode())
    encMessage64 = base64.b64encode(encMessage).decode("utf-8")
    return json.dumps({"data": encMessage64})


class EncryptedDynamicContextBase(DynamicContextModel):
    """Fernet encryption base class. The fields of all models derived from this
    class will be stored in an a encrypted form in the browser"""

    def update(self: Self, **kwargs) -> Self:
        kwargs = decode(**kwargs)
        return super().update(**kwargs)

    def dumps(self, sort_keys=True) -> str:
        plane_text = super().dumps(sort_keys=sort_keys)
        return encode(plane_text)


# Example usage of defining an encrypted user model & context


class UserState(EncryptedDynamicContextBase):
    user_name: str
    password: str


UserContext = create_dynamic_context(UserState)
