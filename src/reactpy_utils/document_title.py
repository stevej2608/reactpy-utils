from reactpy import html, component


@component
def DocumentTitle(title: str):
    """Set the browser tab to the given string"""

    return html.script(
        f"""() => {{
            document.title = "{title}";
        }}"""
    )
