from typing import Any, Callable, TypeVar

# pylint: disable=E1101

T = TypeVar("T")


def static_vars(**kwargs: Any) -> Callable[[T], T]:
    """Add the given kwargs to the given function. This, in effect, assigns
    static values to the function

    Returns:
        Callable[[T], T]: The function with static variables added
    """

    def decorate(func: T) -> T:
        for k, v in kwargs.items():
            setattr(func, k, v)
        return func

    return decorate


@static_vars(counter=0)
def ID() -> int:
    """An immutable counter. Returns  0, 1, 2 ... on each successive call

    Returns:
        int: count 0, 1, 2 ...
    """
    ID.counter += 1  # type: ignore
    return ID.counter  # type: ignore
