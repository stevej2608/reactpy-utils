from typing import Type, TypeVar
from pydantic import BaseModel


from reactpy_router import use_params as _use_params, use_query as _use_query

ParamsClass = TypeVar('ParamsClass', bound=BaseModel)

def use_params(typ:Type[ParamsClass]) -> ParamsClass:
    """Custom version of reactpy_router use_params.

    Returns:
        DotParams: Pydantic version of parameters
    """
    params = _use_params()
    return typ(**params)


def use_query(typ:Type[ParamsClass]) -> ParamsClass:
    """Custom version of reactpy_router use_query.

    Returns:
        DotParams: Pydantic version of query string
    """
    qs = _use_query()
    for key, value in qs.items():
        value = qs[key]
        if isinstance(value, list) and len(value) == 1:
            value = value[0]
            if ' ' in value:
                value = value.split(' ')
            qs[key] = value # type: ignore

    return typ(**qs)
