from reactpy import html, component

IFFY_WRAPPER_JS = """
(function() {
__SCRIPT__
})();       
"""

@component
def IffyScript(script:str, ctx: dict):
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

    if hasattr(ctx, 'model_dump'):
        ctx = ctx.model_dump() # type: ignore

    for k,v in ctx.items():
        script = script.replace(f"{{{k}}}", str(v))

    script = IFFY_WRAPPER_JS.replace('__SCRIPT__', "\n    ".join(script.split('\n')))

    return html.script(script)
