from pathlib import Path
from typing import Callable
from bs4 import BeautifulSoup

TEST_PAGE_FILENAME = "test_page.html"
TEST_PAGE_LIST_FILENAME = "test_page_list.html"

PARAMETERS = {
    'base_url': None,  # provide a link to a page of lists, and replace the number of the page with an asterisk
    'start': 0,  # the first page of lists
    'end': 0,  # the last page of lists
    'provider_name': None,  # name of the provider
    'page_link': None  # provide a link to a specific scholarship page
}


def find_scholarships(soup: BeautifulSoup) -> list:
    return soup.find_all('div', {'class', 'post clearfix'})


def parse_scholarship(scholarship: BeautifulSoup) -> tuple:
    heading = scholarship.find('h2')
    name = None
    link = None

    if heading:
        embedded_link = heading.find('a')

        if embedded_link:
            name = embedded_link.text.strip()
            link = embedded_link['href']

    return name, link  # return the name and link of the scholarship


def scholarships_list_parser(html_text: str) -> dict:
    data_of_all_scholarships = {}
    soup = BeautifulSoup(html_text, 'html.parser')

    scholarships = find_scholarships(soup)

    for scholarship in scholarships:
        name, link = parse_scholarship(scholarship)

        if name and link:
            data_of_all_scholarships[name] = link

    return data_of_all_scholarships


def scholarship_page_parser(html_text: str) -> dict:
    data = {}
    soup = BeautifulSoup(html_text, 'html.parser')

    return data


def test(file_name: str, parser: Callable) -> None:
    with open(Path('data') / PARAMETERS['provider_name'] / file_name, 'r', encoding='utf-8') as file_object:
        html_text = file_object.read()

    print(parser(html_text))


def main():
    test(TEST_PAGE_FILENAME, scholarship_page_parser)
    test(TEST_PAGE_LIST_FILENAME, scholarships_list_parser)


if __name__ == '__main__':
    main()
