from reactpy import component, html
from reactpy.types import VdomChild, VdomChildren


@component
def When(test: bool, *children: VdomChildren) -> VdomChild:
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
