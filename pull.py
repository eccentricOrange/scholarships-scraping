import asyncio
from pathlib import Path
from urllib import request

import aiohttp


def pull_test_page(url: str, base_dir_path: Path, file_name: str) -> None:
    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    my_request = request.Request(url, headers=my_headers)
    html_text = request.urlopen(my_request).read()

    with open(base_dir_path / file_name, 'w', encoding='utf-8') as test_list_file:
        test_list_file.write(html_text.decode('utf-8'))


async def pull_page(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        response_text = await response.text()
        return response_text


async def manage_all_async(urls: list) -> tuple:
    async with aiohttp.ClientSession() as session:
        html_texts = await asyncio.gather(*[pull_page(session, url) for url in urls])
        return html_texts


def run_all_async(urls: list) -> tuple:
    return asyncio.get_event_loop().run_until_complete(manage_all_async(urls))
