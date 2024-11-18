from pydantic import BaseModel
from reactpy import component, use_state

from reactpy_utils.use_query import use_search_params


def component_state(state_type: type[BaseModel]):
    """Component decorator that provides an initialised state object of the
    given type. The object is initialised from the incoming location search string

    Args:
        state_type (_type_): _description_
    """

    def wrapper(func):
        @component
        def wrapped_func(*args, **kwargs):
            page_state, set_page_state = use_state(use_search_params(state_type))

            qs = use_search_params(state_type)
            if page_state != qs:
                set_page_state(qs)
                page_state = qs

            kwargs["state"] = page_state

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper
