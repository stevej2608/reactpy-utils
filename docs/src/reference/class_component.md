# @class_component

While the ReactPy decorator *@component* is used extensively for defining a 
new components there are occasions when it is limiting. The *class_component* 
is a simple decorator that allows any python class to behave as a component. 

An example of it's use would be a Table class which encapsulates table data
together with methods that return several views: pagination, 
search, filter, etc. A table instance, once created, can be used in different
parts of the UI. The search view in the header section, the pagination view 
above or below the table body and a summary view on the 
dashboard for instance. Each of these views would be implemented in the methods of the 
Table class.

```
@class_component
class MyTable:

    def __init__(self, table_data):
        ...

    def search(self, test:str):
        ...

    def paginator(self, test:str):
        ...

    def summary(self, test:str):
        ...       

    def render(self):
        """The default view"""
        ...
```
