from reactpy import html, component


@component
def DocumentTitle(title: str):
    return html.script(
        f"""() => {{
            document.title = "{title}";
        }}"""
    )
