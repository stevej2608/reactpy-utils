import os
from pathlib import Path

import pytest
from dotenv import get_key, set_key


def update_vscode_env(env_file_path: str) -> None:  # pragma: no cover
    """
    Create/update the .env file PATH entry. The entry is prefixed with the 'hatch
    test' path of the currently executing test session.

    If the 'env_file_path' already contains a reference to a hatch-test virtual env the update is dismissed.

    The PATH entry in the .env file is used by the VSCODE debugger to launch the tests
    in the same environment as hatch uses.
    """

    dotenv_path = Path(env_file_path)
    paths = os.environ["PATH"].split(":")

    for path in paths:
        if "hatch-test" in path:
            value = get_key(dotenv_path, "PATH")
            if value is None or "hatch-test" not in value:
                dotenv_path.touch(mode=0o600, exist_ok=True)
                # Save path to the file.
                value = f"{path}:${{PATH}}"
                set_key(dotenv_path=dotenv_path, key_to_set="PATH", value_to_set=value)

            return

    # We must be running in VSCODE debugger with no hatch-test path reference
    # set, issue a warning and exit pytest.

    pytest.exit(
        "Unable to find reference to the 'hatch-test' virtual environment in env $PATH\n"
        "Run 'hatch test' or edit .env file manually before running tests again."
    )
