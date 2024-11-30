from reactpy import component

from reactpy_utils import DocumentTitle


@component
def App():
    return DocumentTitle("My Website")
