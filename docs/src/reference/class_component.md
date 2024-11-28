# @class_component

While the ReactPy decorator *@component* is used extensively for defining a 
new components there are occasions when it is limiting. The *class_component* 
is a simple decorator that allows any python class to behave as a component. 

An example of its use would be a Table class which encapsulates table data
together with methods that return several views: pagination, 
search, filter, etc. A table instance, once created, can be used in different
parts of the UI. The search view in the header section, the pagination view 
above or below the table body and a summary view on the 
dashboard for instance. Each of these views would be implemented in the methods of the 
Table class.

A comprehensive implementation of a table base class containing the carefully 
honed logic for pagination, search & filtering, say, could then be subclassed to
provide various UI implementations or override aspects of the table logic.

=== "class_component.py"

    ```python
    {% include "../../examples/python/class_component.py" %}
    ```
