from reactpy import component, html

from reactpy_utils.script import Script

COPY_TO_CLIPBOARD_JS = """
    () => {

        function copy_to_clipboard() {

            // Get the text field

            var element = document.getElementById('{text_id}');

            if (element) {

                // Select the text field

                const value = element.getAttribute('data-clipboard-content');

                // Copy the text to the clipboard

                navigator.clipboard.writeText(value);
            }
            else {
                console.error('click: btn-{button_id}, error  #{text_id} missing');
            }
        }

        const button = document.getElementById('{button_id}');
        button.addEventListener('click', copy_to_clipboard);

        return () => {
            button.removeEventListener('click', copy_to_clipboard);
        }

    }
"""


@component
def CopyToClipboard(button_id: str, text: str):
    """Attach copy-to-clipboard' action to button of given 'button_id' that, when clicked, will copy the given text to the clipboard.

    Args:
        button_id (str): The button to be listened to
        text (str): The text to be copied

    Returns:
        _type_: _description_

    Example:
    ```
    BUTTON_ID = "copy-btn"
    TEXT = lorem.paragraph()


    @component
    def App():
        return html._(
            html.button({"id": BUTTON_ID}, "Copy to Clipboard"),
            CopyToClipboard(button_id=BUTTON_ID, text=TEXT),
        )
    ```
    """

    ctx = {"button_id": f"{button_id}", "text_id": f"{button_id}-text"}

    return html._(
        html.div({"id": ctx["text_id"], "data-clipboard-content": text, "hidden": True}),
        Script(COPY_TO_CLIPBOARD_JS, ctx, minify=True),
    )
