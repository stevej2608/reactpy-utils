A browser local storage provider. Synchronizes the given context model with the browser local storage. The
provider blocks the rendering of any child components until the the model has been 
synchronized with the browser.

The context model is stored in the browser's local storage as unencrypted stringified json.

=== "local_storage.py"

    ```python
    {% include "../../examples/python/local_storage.py" %}
    ```

=== "app_context.py"

    ```python
    {% include "../../examples/python/app_context.py" %}
    ```

## Encrypting Local Storage Data

The data stored in the browser can easily be encrypted by sub-classing *DynamicContextModel*. The 
following example uses [Fernet] symmetric encryption. 

Use *Fernet.generate_key()* to create keys. The key remains on the server, only encrypted 
data is sent to the browser.

=== "encrypted_app_context.py"

    ```python
    {% include "../../examples/python/encrypted_app_context.py" %}
    ```

The same pattern can be applied to any desired encryption method.

[Fernet]: https://cryptography.io/en/latest/fernet/