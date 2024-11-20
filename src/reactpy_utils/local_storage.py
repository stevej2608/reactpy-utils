import json
import logging
from typing import cast

from reactpy import component, event, html, use_context
from reactpy.core.component import Component

from reactpy_utils.dynamic_context import DynamicContextModel
from reactpy_utils.script import Script
from reactpy_utils.types import EventArgs
from reactpy_utils.when import When

log = logging.getLogger(__name__)


LOCAL_STORAGE_READ_JS = """
    () => {
        const storage = document.querySelector('#{local_storage_id}');

        if (!storage) {
            console.error('Local storage reader element not found');
            return;
        }

        // Set the value of the storage element

        const value = localStorage.getItem('{local_storage_id}') || "undefined";

        if (value == "undefined") {
            localStorage.setItem('{local_storage_id}', storage.value);
        }
        else {
            storage.value = value;
        }

        storage.click();

    }
"""


@component
def _LocalStorageReader(ctx, storage_id: str):
    """Read the browsers local storage and update LocalStorageContext"""

    # The value attribute of a hidden <textarea> element is used as a buffer to
    # communicate the value of an associated localStorage element. If the
    # value held in localStorage is different to the value in the
    # textarea the script copies the value to the text area and forces
    # a click event on the <textarea> element.

    # The localStorage JSON values are available to the reactpy on_click()
    # event handler. These values are used to update the given context.

    # The on_click() update will only occur once during start-up. During
    # normal operation the the browser localStorage is kept in sync by
    # LocalStorageWriter(), see below.

    storage, set_storage = use_context(ctx)

    storage = cast(DynamicContextModel, storage)

    # log.info('LSReader storage=[%s]', storage.__repr__())

    @event(stop_propagation=True, prevent_default=True)
    def on_click(_evt: EventArgs):
        data = _evt["target"]["value"].replace("-", "_")
        data = json.dumps(json.loads(data))
        values = json.loads(data)
        set_storage(storage.update(**values))

    # log.info('LocalStorageReader.render() %s', id)

    return html._(
        html.textarea({"hidden": True, "id": storage_id, "value": storage.dumps(), "on_click": on_click}),
        When(not storage.is_valid, Script(LOCAL_STORAGE_READ_JS, {"local_storage_id": storage_id}, minify=True)),
    )


LOCAL_STORAGE_WRITE_JS = """
    () => {
        // Write values to localStorage

        try {
            //  console.log('write {local_storage_id} values: {values}');
            localStorage.setItem('{local_storage_id}', '{values}');

        } catch (error) {
            // Handle potential localStorage errors (e.g., storage quota exceeded, private browsing)
            console.error('Error writing to localStorage({local_storage_id}):', error);
        }
    }
"""


@component
def _LocalStorageWriter(ctx, storage_id: str):
    storage, _ = use_context(ctx)

    @component
    def write_script(state: DynamicContextModel):
        if state.is_valid:
            # log.info('Write id=%s, ctx=%s', id, state.dumps())
            ctx = {"local_storage_id": storage_id, "values": state.dumps()}
            return Script(LOCAL_STORAGE_WRITE_JS, ctx, minify=True)
        return None

    return html._(write_script(storage))


@component
def LocalStorageAgent(ctx: DynamicContextModel, storage_key: str):
    """Browser local storage agent. Synchronies the given model
    with the browser local storage

    Args:
        ctx (DynamicContextModel): The values to be stored
        storage_key (str): The browser local storage key

    Returns:
        Component: The local storage agent
    """
    return html._(
        _LocalStorageWriter(ctx, storage_key),
        _LocalStorageReader(ctx, storage_key),
    )


@component
def LocalStorageProvider(*children: tuple[Component], ctx: DynamicContextModel, storage_key: str):
    """Wrapper for LocalStorageAgent component. Children are not rendered until the 
    given context has been synchronized with the browser local storage.

    Args:
        ctx (DynamicContextModel): The model to be synchronized with local storage
        storage_key (str): The browser local storage key

    Returns:
        Component: The local storage provider
    """
    storage, _ = use_context(ctx)  # type: ignore
    return html._(
        LocalStorageAgent(ctx=ctx, storage_key=storage_key),
        When(storage.is_valid, *children),
    )
