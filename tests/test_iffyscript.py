from reactpy_utils.iffy_script import IffyScript

IFRAME_UPDATE_JS = """
    var iFrame = document.getElementsByClassName('{iframe_code}')[0];

    function iframe_update() {

        // Toggle dark mode

        var theme = {dark_mode}

        let html = iFrame.contentDocument.querySelector('html');
        if (theme) {
            html.classList.add('dark');
        } else {
            html.classList.remove('dark');
        }

        // Bump the iframe height if needed

        let attempts = 30;

        const interval = setTimeout(() => {
            try {
                const height = iFrame.contentWindow.document.body.scrollHeight + 20;
                iFrame.style.height = height + 'px';
                clearInterval(interval);
            } catch (e) {
                if (--attempts <= 0) {
                    clearInterval(interval);
                    console.warn('Failed to set iframe height');
                }
            }

        }, 100);

    }; 

    try {
        iframe_update();
    }
    catch(err) {
        iFrame.onload = iframe_update;
    }

"""

POPPER_JS = """
const button = document.querySelector('#{target_id}');
const tooltip = document.querySelector('#{tooltip_id}');

const popperInstance = Popper.createPopper(button, tooltip, {
  placement: '{placement}',
  modifiers: [{
    name: 'offset',
    options: {
      offset: [0, 8],
    },
  }, ],
});

function show() {
  // Make the tooltip visible
  tooltip.classList.remove("hidden");

  // Enable the event listeners
  popperInstance.setOptions((options) => ({
    ...options,
    modifiers: [
      ...options.modifiers,
      {
        name: 'eventListeners',
        enabled: true
      },
    ],
  }));

  // Update its position
  popperInstance.update();
};

function hide() {
  // Hide the tooltip
  tooltip.classList.add("hidden");

  // Disable the event listeners
  popperInstance.setOptions((options) => ({
    ...options,
    modifiers: [
      ...options.modifiers,
      {
        name: 'eventListeners',
        enabled: false
      },
    ],
  }));
};

const showEvents = ['mouseenter', 'focus'];
const hideEvents = ['mouseleave', 'blur'];

showEvents.forEach((event) => {
  button.addEventListener(event, show);
});

hideEvents.forEach((event) => {
  button.addEventListener(event, hide);
});
"""


def xtest_simple():

    script = IffyScript(IFRAME_UPDATE_JS, {"dark_mode":True,"iframe_code":"iframe-code-100","tw_class":"dark"}).render()

    lines = script['children'][0].split('\n') # type: ignore

    assert lines[9] == '            var theme = true'
    assert lines[46] == '})();'


def test_IFRAME_UPDATE_JS_minified():

    script = IffyScript(
        IFRAME_UPDATE_JS,
        {"dark_mode":True,"iframe_code":"iframe-code-100","tw_class":"dark"},
        minify=True
        ).render()

    script = str(script['children'][0]) # type: ignore
    assert len(script) == 593


def xtest_POPPER_JS_minified():

    script = IffyScript(
        POPPER_JS,{
            "tid":"tooltip-aba8f7f7",
            "placement":"top",
            "target_id":"tooltip-aba8f7f7-target",
            "tooltip_id":"tooltip-aba8f7f7-tooltip"
         },
        minify=False
        ).render()

    script = str(script['children'][0]) # type: ignore
    assert len(script) == 592
