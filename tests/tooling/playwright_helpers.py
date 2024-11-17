
import json
from reactpy_utils import DynamicContextModel, create_dynamic_context


class AppState(DynamicContextModel):
    dark_mode: bool = True

AppContext = create_dynamic_context(AppState)


async def read_local_storage(page, key:str):
    # https://scrapingant.com/blog/playwright-local-storage
    # Access Local Storage data
    local_storage_data = await page.evaluate("""() => {
        return localStorage.getItem('{key}');
    }""".replace('{key}', key))

    data = json.dumps(json.loads(local_storage_data))
    return data



async def get_document_title(page):

    title = await page.evaluate("""() => {
        return document.title;
    }""")

    return title
