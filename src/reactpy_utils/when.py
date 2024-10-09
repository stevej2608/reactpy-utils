from typing import Tuple
from reactpy import component, html
from reactpy.core.component import Component

@component
def When(test:bool, *children: Tuple[Component]):
    """Show children when test is true

    Returns:
        html._(): Return a fragment containing the children
    """

    if test:
        return html._(*children)
    else:
        return None
