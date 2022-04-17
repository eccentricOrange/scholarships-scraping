from asyncio import gather, get_event_loop, TimeoutError
from pathlib import Path
from urllib import request

from aiohttp import ClientSession, TCPConnector

# pull one page
# this will be used by the user to test the parser they're writing
# this is synchronous, and will only ever be run once at a time
def pull_test_page(url: str, base_dir_path: Path, file_name: str) -> None:
    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    my_request = request.Request(url, headers=my_headers)
    html_text = request.urlopen(my_request).read()

    with open(base_dir_path / file_name, 'w', encoding='utf-8') as test_list_file:
        test_list_file.write(html_text.decode('utf-8'))

# pull one page, as part of the async process
async def pull_page(session: ClientSession, url: str) -> str:
    try:
        async with session.get(url) as response:
            response_text = await response.text()
            return response_text

    except TimeoutError:
        return ""

# pull all pages, asynchronously
# handle sessions and TCP connections
async def manage_all_async(urls: list) -> tuple:
    async with ClientSession(connector=TCPConnector(force_close=True)) as session:
        html_texts = await gather(*[pull_page(session, url) for url in urls])
        return html_texts

# run the async stuff
def run_all_async(urls: list) -> tuple:
    return get_event_loop().run_until_complete(manage_all_async(urls))
