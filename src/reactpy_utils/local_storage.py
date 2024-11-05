from typing import cast
import json
from reactpy import component, event, html, use_context

from .types import EventArgs
from .dynamic_context import DynamicContextModel
from .iffy_script import IffyScript


# https://stackoverflow.com/questions/24278469/click-a-button-programmatically-js
# https://stackoverflow.com/questions/47240315/how-to-update-input-from-a-programmatically-set-textarea

LOCAL_STORAGE_READ_JS = """
    const storage = document.querySelector('#{local_storage_id}');
    
    if (!storage) {
        console.error('Local storage reader element not found');
        return;
    }

    // Set the value of the storage element

    storage.value = localStorage.getItem('{local_storage_id}') || "{}";
    
    console.log('Storage read:', storage.value);
    
    // Trigger click event

    storage.click();
"""

LOCAL_STORAGE_WRITE_JS = """
    // Write values to localStorage

    try {
        localStorage.setItem('{local_storage_id}', '{values}');

    } catch (error) {
        // Handle potential localStorage errors (e.g., storage quota exceeded, private browsing)
        console.error('Error writing to localStorage({local_storage_id}):', error);
    }
"""

@component
def LocalStorgeReader(ctx, id:str):
    """Read the browsers local storage and update LocalStorageContext"""

    storage, set_storage = use_context(ctx)

    storage = cast(DynamicContextModel, storage)

    # log.info('LSReader storage=[%s]', storage)

    @event
    def on_click(event:EventArgs):
        data = event["target"]["value"].replace('-', '_')
        # log.info('on_click data=[%s]', data)

        data = json.dumps(json.loads(data))
        if data != storage.dumps() or not storage.is_valid:
            # log.info('update storage')
            values = json.loads(data)
            set_storage(storage.update(**values))

    return html._(
        html.textarea({"class_name": "hidden", "id": id, "value": storage.dumps(),"on_click": on_click}),
        IffyScript(LOCAL_STORAGE_READ_JS, {'local_storage_id': id})
    )

@component
def LocalStorgeWriter(ctx, id:str):
    storage, _ = use_context(ctx)

    # log.info('LSWriter storage=[%s]', storage)

    @component
    def write_script(state: DynamicContextModel):
        if state.is_valid:
            return IffyScript(LOCAL_STORAGE_WRITE_JS, {'local_storage_id' :id,'{values}' : state.dumps()})

    return html._(
        write_script(storage)
    )


@component
def LocalStorageAgent(ctx: DynamicContextModel, storage_key:str):
    """Browser local storage agent. Syncronises the given modle 
    with the browser local storage

    Args:
        ctx (DynamicContextModel): The values to be stored
        storage_key (str): local storage key

    Returns:
        _type_: _description_
    """
    return html._(
        LocalStorgeReader(ctx, storage_key),
        LocalStorgeWriter(ctx, storage_key),
    )
