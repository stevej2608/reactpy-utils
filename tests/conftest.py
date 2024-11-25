import subprocess

import pytest
from playwright.async_api import Browser, Page, async_playwright
from reactpy.config import REACTPY_TESTING_DEFAULT_TIMEOUT
from reactpy.testing import BackendFixture, DisplayFixture

from .tooling import update_vscode_env


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--headed",
        dest="headed",
        action="store_true",
        help="Open a browser window when running web-based tests",
    )


def pytest_sessionstart(session):
    """Rebuild the project before running the tests to get the latest JavaScript"""

    # subprocess.run(["hatch", "build", "--clean"], check=True)

    update_vscode_env(".env")
    subprocess.run(["playwright", "install", "chromium"], check=True)


@pytest.fixture(scope="session")
async def display(server: BackendFixture, page: Page):
    async with DisplayFixture(server, page) as display:
        yield display


@pytest.fixture(scope="session")
async def server():
    async with BackendFixture() as server:
        yield server


@pytest.fixture(scope="session")
async def page(browser: Browser):
    context = await browser.new_context(permissions=["clipboard-read", "clipboard-write"])
    pg = await context.new_page()
    pg.set_default_timeout(REACTPY_TESTING_DEFAULT_TIMEOUT.current * 1000)
    try:
        yield pg
    finally:
        await pg.close()


@pytest.fixture(scope="session")
async def browser(pytestconfig: pytest.Config):
    async with async_playwright() as pw:
        yield await pw.chromium.launch(headless=not bool(pytestconfig.option.headed))
