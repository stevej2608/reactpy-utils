Custom versions of reactpy_router use_search_params that return parameters as a 
[Pydantic] data class.


## use_search_params 

The following search params can be converted into a Pydantic model 
as follows.

    ?hello=world&thing=1&thing=2

```
from pydantic import BaseModel
from reactpy import component, html

from reactpy_utils import use_search_params

class MyParams(BaseModel):
    hello: str | None = None
    thing: list[int] | None = None


@component
def App():
    params = use_search_params(MyParams)

    return html.h2(params.hello)
```

# use_params 


[Pydantic]: https://docs.pydantic.dev/latest/