import re
from reactpy import html, component


IFFY_WRAPPER_JS = """
(function() {
__SCRIPT__
})();
"""


def minify_javascript(source_code):
    """
    Minifies JavaScript source code by removing unnecessary whitespace, comments, and newlines.
    
    Args:
        source_code (str): The JavaScript source code to minify
        
    Returns:
        str: Minified JavaScript code
    """
    # Remove multi-line comments
    source_code = re.sub(r'/\*[\s\S]*?\*/', '', source_code)

    # Remove single-line comments
    source_code = re.sub(r'//.*$', '', source_code, flags=re.MULTILINE)

    # Preserve strings
    # strings = []
    # def preserve_string(match):
    #     strings.append(match.group(0))
    #     return f'__STRING_{len(strings)-1}__'

    # Store strings temporarily
    # source_code = re.sub(r'(["\'])(?:(?!\1).|\\.)*\1', preserve_string, source_code)

    # Remove whitespace
    source_code = re.sub(r'\s+', ' ', source_code)             # Convert multiple spaces to single space
    # source_code = re.sub(r'^\s+|\s+$', '', source_code)       # Trim start and end
    source_code = re.sub(r'\s*([{};,:])\s*', r'\1', source_code)  # Remove space around special chars
    source_code = re.sub(r'\s*([=+\-*/<>])\s*', r'\1', source_code)  # Remove space around operators

    # Restore strings
    # for i, string in enumerate(strings):
    #     source_code = source_code.replace(f'__STRING_{i}__', string)

    return source_code



@component
def IffyScript(script:str, ctx: dict, fix_bools=True, minify=False):
    """Minimal template engine that replaces values in given script template, wrapping the 
    script in an iffy. The script is returned as a html.script() element
    
    Example:
    ```
    localStorage.setItem('{local_storage_id}', '{value}');
    ```

    Is converted to

    ```
    (function() {

        localStorage.setItem('theme', 'dark');

    })();
    ```
    
    """

    def indent(text:str):
        lines = []
        for line in text.split('\n'):
            line = line if line == "" else "    " + line
            lines.append(line.rstrip())
        return '\n'.join(lines)


    if hasattr(ctx, 'model_dump'):
        ctx = ctx.model_dump() # type: ignore

    for k,v in ctx.items():

        if isinstance(v, bool) and fix_bools:
            v = str(v).lower()

        script = script.replace(f"{{{k}}}", str(v))

    if not minify:
        script = indent(script)
        script = IFFY_WRAPPER_JS.replace('__SCRIPT__', script)
    else:
        script = IFFY_WRAPPER_JS.replace('__SCRIPT__', script)
        script = minify_javascript(script)
        print(f"\n\n\n{script}")
    return html.script(script)
