Browser local storage provider. Synchronizes the given context model with the browser local storage. The
provider blocks the rendering of any child components until the the model has been 
synchronized with the browser.

The context model is stored in the browser's local storage as unencrypted stringified json.

=== "docs/examples/local_storage.py"

    ```python
    {% include "../../examples/python/local_storage.py" %}
    ```

## Encrypting the data

The local storage provider expects the context model to be derived 
from *DynamicContextModel*.

TODO: Example of Encrypting the data