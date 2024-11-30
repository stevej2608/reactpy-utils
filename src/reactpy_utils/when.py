from reactpy import component, html
from reactpy.core.component import Component
from reactpy.core.types import VdomChild


@component
def When(test: bool, *children: tuple[Component]) -> VdomChild:
    """Render children when test is True

    Args:
        test (bool): _description_

    Returns:
        Component: Return a fragment containing the child components

    Returns:
        Component: Return a fragment containing the child components

    Example
    ```
    @component
    def App():
        return AppContext(When(app_state.is_valid, MainPage()))
    ```
    """

    if test:
        return html._(*children)
    return None
