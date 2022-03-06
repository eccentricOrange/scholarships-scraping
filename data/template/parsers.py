from pathlib import Path
from bs4 import BeautifulSoup as Soup

TEST_PAGE_FILENAME = "test_page.html"
TEST_PAGE_LIST_FILENAME = "test_page_list.html"

PARAMETERS = {
    'base_url': None,  # provide a link to a page of lists, and replace the number of the page with an asterisk
    'start': 0,  # the first page of lists
    'end': 0,  # the last page of lists
    'provider_name': None,  # name of the provider
    'page_link': None  # provide a link to a specific scholarship page
}


def find_scholarships(soup: Soup) -> list:
    return soup.find_all('div', {'class', 'post clearfix'})


def parse_scholarship(scholarship: Soup) -> tuple:
    heading = scholarship.find('h2')

    return None, None  # return the name and link of the scholarship


def scholarships_list_parser(html_text: str) -> list:
    data_of_all_scholarships = []
    soup = Soup(html_text, 'html.parser')

    scholarships = find_scholarships(soup)

    for scholarship in scholarships:
        name, link = parse_scholarship(scholarship)
        data_of_current_scholarship = {}

        if name and link:
            data_of_current_scholarship['name'] = name
            data_of_current_scholarship['link'] = link

            data_of_all_scholarships.append(data_of_current_scholarship)

    return data_of_all_scholarships


def scholarship_page_parser(html_text: str) -> dict:
    data = {}
    soup = Soup(html_text, 'html.parser')

    return data


def test(file_name: str, parser):
    with open(Path('data') / PARAMETERS['provider_name'] / file_name, 'r', encoding='utf-8') as file_object:
        html_text = file_object.read()

    print(parser(html_text))


if __name__ == '__main__':
    test(TEST_PAGE_FILENAME, scholarship_page_parser)
    test(TEST_PAGE_LIST_FILENAME, scholarships_list_parser)
