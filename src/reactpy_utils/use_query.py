from typing import TypeVar

from pydantic import BaseModel
from reactpy_router import use_params as _use_params
from reactpy_router import use_search_params as _use_search_params

ParamsClass = TypeVar("ParamsClass", bound=BaseModel)


def use_params(typ: type[ParamsClass]) -> ParamsClass:
    """Custom version of reactpy_router use_params.

    Returns:
        DotParams: Pydantic version of parameters
    """
    params = _use_params()
    return typ(**params)


def use_search_params(typ: type[ParamsClass]) -> ParamsClass:
    """Custom version of reactpy_router use_search_params.

    Returns:
        DotParams: Pydantic version of query string
    """
    qs = _use_search_params()
    for key, value in qs.items():
        if isinstance(value, list) and len(value) == 1:
            value = value[0]
            if " " in value:
                value = value.split(" ")
            qs[key] = value  # type: ignore

    return typ(**qs)
