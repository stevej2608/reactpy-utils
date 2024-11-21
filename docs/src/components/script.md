The *Script* component wraps the RectPy *html.script()* to provide support for variable 
substitution and minification.

Script example:

```python
from reactpy_utils import Script, IDynamicContextModel

def save_state(storage_id:str, state: IDynamicContextModel):
    ctx = {"local_storage_id": storage_id, "values": state.dumps()}
    return Script(LOCAL_STORAGE_WRITE_JS, ctx, minify=True)

LOCAL_STORAGE_WRITE_JS = """
    () => {
        // Write values to localStorage

        try {
            console.log('write {local_storage_id} values: {values}');
            localStorage.setItem('{local_storage_id}', '{values}');

        } catch (error) {
            // Handle potential localStorage errors (e.g., storage quota exceeded, private browsing)
            console.error('Error writing to localStorage({local_storage_id}):', error);
        }
    }
"""
```
### Minification

The minimal minification process will, if enabled, strip white space, comments and 
console.log() messages from the source. The minification process is pretty dumb. Semicolons
at the end of statements are important. If your script fails when minified check first
for missing semicolons.

### Script Life Cycle

Scripts are injected and run when the associated page is loaded. If the script hooks into event 
listeners or other state-related aspects of the DOM then these must be un-hooked when the page
is destroyed. This can be achieved by returning a *page-unload* function reference when the script is first
loaded. To do this define a script with the following pattern:

```python
SCRIPT_WITH_CLEAN_UP_JS = """
    () => {

        // Code executed when page is loaded

        return () => {
            // Code executed when page is unloaded
        }

    }
"""
```

### Debugging Scripts

Scripts can be debugged using the Browser debugger (or directly in VSCODE). To locate
the code add a `console.log("My Code Loaded")` message to the script. This will appear
in the debugger console window. Clicking on it will take you directly to your code. Add
brake points as required.


[RectPy]: https://reactpy.dev/docs/index.html
