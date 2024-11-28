from reactpy import component, html
from reactpy.core.component import Component


@component
def When(test: bool, *children: tuple[Component]):
    """Render children when test is True

    Returns:
        Component: Return a fragment containing the child components

    Example
    ```
    @component
    def App():
        return AppContext(
            When(app_state.is_valid, MainPage())
        )
    ```
    """

    if test:
        return html._(*children)
    return None
