from pydantic import BaseModel

from reactpy_utils import Script

TEST_JS = """
    /**
     * Multiline to be removed on minify
     */

    () => {
        // Comment to be removed on minify
        console.log("XXX");
        const enabled = {enabled}
        const storage = document.querySelector('#{id}');
    }
"""


def test_script():
    # Test un-minified

    script = Script(TEST_JS, {"id": "test", "enabled": True}).render()
    script_body: str = script["children"][0]  # type: ignore

    assert script_body
    assert "#test" in script_body
    assert "enabled = true" in script_body
    assert len(script_body.split("\n")) == 12

    assert True


def test_script_minified():
    class Params(BaseModel):
        id: str = "test"
        enabled: bool = False

    script = Script(TEST_JS, Params(), minify=True).render()
    script_body: str = script["children"][0]  # type: ignore

    assert script_body
    assert "#test" in script_body
    assert "enabled=false" in script_body
    assert len(script_body) == 72

    assert True
