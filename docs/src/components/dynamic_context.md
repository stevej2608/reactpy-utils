The *dynamic context model* is an enhanced version of the ReactPy [use-context] hook. In addition
to providing application state that can be easily accessed by child components the 
*dynamic context model* allows the child components to change the state. Any changes
made by a child component will update the context and will force the parent component
and children to be re-rendered.

A typical usage would be where a deeply embedded child component, a drop-down element in
a complex nested navigation component say, needs to update some element in 
the main application state. 


=== "dynamic_context.py"

    ```python hl_lines="8 9 12 17 30 34"
    {% include "../../examples/python/dynamic_context.py" %}
    ```

=== "app_context.py"

    ```python
    {% include "../../examples/python/app_context.py" %}
    ```

[use-context]: https://reactpy.dev/docs/reference/hooks-api.html#use-context


## Custom Context Models

By default context models are defined by sub-classing *DynamicContextModel* which
itself is a subclass of the [Pydantic], [BaseModel]. As an alternative you can also
subclass the none-pydantic *CustomDynamicContextModel* or implement the protocol
interface *IDynamicContextModel*


```python
from reactpy_utils import CustomDynamicContextModel, create_dynamic_context

class CurrentUserState(CustomDynamicContextModel):

    def __init__(self, user_name: str, password:str, dark_mode: bool = True):
        super().__init__()
        self.user_name = user_name
        self.password = password
        self.dark_mode = dark_mode


AppContext = create_dynamic_context(CurrentUserState)
```

[Pydantic]: https://docs.pydantic.dev/latest/
[BaseModel]: https://docs.pydantic.dev/latest/api/base_model/
