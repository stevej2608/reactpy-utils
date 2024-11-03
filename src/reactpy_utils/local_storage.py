import json
from reactpy import component, event, html, use_context

from .types import EventArgs
from .dynamic_context import DynamicContextModel


# https://stackoverflow.com/questions/24278469/click-a-button-programmatically-js
# https://stackoverflow.com/questions/47240315/how-to-update-input-from-a-programmatically-set-textarea

LOCAL_STORAGE_READ_JS = """
    (function() {

        const storage = document.querySelector('#local-storage-reader');
        
        if (!storage) {
            console.error('Local storage reader element not found');
            return;
        }

        const values = Object.create(null);

        // Iterate through localStorage keys

        for (let i = 0; i < localStorage.length; i++) {
            const storageKey = localStorage.key(i);
            
            // Only add if key exists
            if (storageKey) {
                values[storageKey] = localStorage.getItem(storageKey);
            }
        }

        // Set the value of the storage element

        storage.value = JSON.stringify(values);
        
        console.log('Storage read:', storage.value);
        
        // Trigger click event

        storage.click();
    })();
"""

LOCAL_STORAGE_WRITE_JS = """
    (function() {
        // Initial values object
        const values = {values}

        // Log the initial values

        console.log('Storage write:', JSON.stringify(values));

        // Write values to localStorage

        try {
            // Use Object.entries to iterate through key-value pairs
            for (const [key, value] of Object.entries(values)) {
                localStorage.setItem(key, value);
            }
        } catch (error) {
            // Handle potential localStorage errors (e.g., storage quota exceeded, private browsing)
            console.error('Error writing to localStorage:', error);
        }
    })();
"""

@component
def LocalStorgeReader(ctx):
    """Read the browsers local storage and update LocalStorageContext"""

    storage, set_storage = use_context(ctx)

    # log.info('LSReader storage=[%s]', storage)

    @event
    def on_click(event:EventArgs):
        data = event["target"]["value"].replace('-', '_')
        # log.info('on_click data=[%s]', data)

        data = json.dumps(json.loads(data))
        if data != storage.dumps() or storage.update_count == 0:
            # log.info('update storage')
            values = json.loads(data)
            set_storage(storage.update(**values))

    return html._(
        html.textarea({"class_name": "hidden", "id": "local-storage-reader", "value": storage.dumps(),"on_click": on_click}),
        html.script(LOCAL_STORAGE_READ_JS)
    )

@component
def LocalStorgeWriter(ctx):
    storage, _ = use_context(ctx)

    # log.info('LSWriter storage=[%s]', storage)

    @component
    def write_script(state: DynamicContextModel):

        if state.is_valid:
            # log.info('LSWriter update storage=[%s]', state.dumps())
            script = LOCAL_STORAGE_WRITE_JS
            script = script.replace("{values}", state.dumps())
            return html.script(script)

    return html._(
        write_script(storage)
    )


@component
def LocalStorageAgent(ctx):
    return html._(
        LocalStorgeReader(ctx),
        LocalStorgeWriter(ctx),
    )
