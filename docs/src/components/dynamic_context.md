The *dynamic context model* is an enhanced version of the ReactPy [use-context] hook. In addition
to providing application state that can be easily accessed by child components 
*dynamic context model* allows the child components to change the state. Any changes
made by a child component will update the context and will force the parent component
and children to be re-rendered.

A typical usage would be where a deeply embedded child component, a drop-down element in
a complex nested navigation component say, needs to update some element in 
the main application state. 


=== "docs/examples/python/dynamic_context.py"

    ```python hl_lines="8 9 12 17 30 34"
    {% include "../../examples/python/dynamic_context.py" %}
    ```

=== "docs/examples/app_context.py"

    ```python
    {% include "../../examples/python/app_context.py" %}
    ```

[use-context]: https://reactpy.dev/docs/reference/hooks-api.html#use-context
