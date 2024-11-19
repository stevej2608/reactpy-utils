import logging
import re

from reactpy import component, html

log = logging.getLogger(__name__)


def minify_javascript(source_code):
    """
    Minifies JavaScript source code by removing unnecessary whitespace, comments, and newlines.

    Args:
        source_code (str): The JavaScript source code to minify

    Returns:
        str: Minified JavaScript code
    """
    # Remove multi-line comments

    source_code = re.sub(r"/\*[\s\S]*?\*/", "", source_code)

    # Remove single-line comments

    source_code = re.sub(r"//.*$", "", source_code, flags=re.MULTILINE)

    # Remove console.log messages

    source_code = re.sub(r"console\.log.*$", "", source_code, flags=re.MULTILINE)

    # Convert multiple spaces to single space

    source_code = re.sub(r"\s+", " ", source_code)

    # Remove space around special chars

    source_code = re.sub(r"\s*([{};,:])\s*", r"\1", source_code)

    # Remove space around operators

    source_code = re.sub(r"\s*([=+\-*/<>])\s*", r"\1", source_code)

    return source_code.lstrip()


@component
def Script(script: str, ctx: dict, fix_bools=True, minify=False):
    """Minimal script wrapper with template engine that replaces values in given script template"""

    if hasattr(ctx, "model_dump"):
        ctx = ctx.model_dump()  # type: ignore

    for k, v in ctx.items():
        if isinstance(v, bool) and fix_bools:
            v = str(v).lower()

        script = script.replace(f"{{{k}}}", str(v))

    if minify:
        script = minify_javascript(script)

    return html.script(script)
