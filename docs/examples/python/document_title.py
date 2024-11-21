import lorem
from reactpy import component, html

from reactpy_utils import DocumentTitle


@component
def App():
    return html._(
        DocumentTitle('My Website')
    )
