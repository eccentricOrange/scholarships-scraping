from json import load
from multiprocessing import Pool
from typing import Callable

from data.template.parsers import (PARAMETERS, TEST_PAGE_FILENAME,
                                   TEST_PAGE_LIST_FILENAME,
                                   scholarship_page_parser,
                                   scholarships_list_parser)
from modules.fileio import (create_links_list, create_scholarship_links,
                            get_headers, setup, store, write_values)
from modules.pull import pull_test_page, run_all_async

LINKS_FILENAME = 'links.json'
SCHOLARSHIPS_FILENAME = 'scholarships.json'
CSV_FILENAME = 'scholarships.csv'


def collect_all_scholarships(lists_of_lists: list) -> list:
    scholarships = []

    for list_of_scholarships in lists_of_lists:
        for scholarship, link in list_of_scholarships.items():
            scholarships.append({'name': scholarship, 'link': link})

    return scholarships


def pull_scholarship_page_test() -> None:
    print("Starting download of schoalrship test page...")
    pull_test_page(PARAMETERS['page_link'],
                   PARAMETERS['base_path'], TEST_PAGE_FILENAME)
    print("Finished download of scholarship test page.\n")


def pull_list_page_test() -> None:
    print("Starting download of list test page...")
    pull_test_page(PARAMETERS['base_url'].replace(
        '*', str(PARAMETERS['start'])), PARAMETERS['base_path'], TEST_PAGE_LIST_FILENAME)
    print("Finished download of list test page.\n")


def parse_all(html_texts: tuple, parse_one_function: Callable[[str], dict]) -> list:
    pool = Pool()
    return pool.map(parse_one_function, list(html_texts))


def get_list_of_scholarships() -> None:
    links_with_scholarships = create_links_list(
        PARAMETERS['base_url'], PARAMETERS['end'], PARAMETERS['start'])
    print(f"{len(links_with_scholarships)} pages of scholarship lists to be downloaded.\n")
        
    print("Starting downloads for lists of scholarships...")
    htmls_of_scholarships = run_all_async(links_with_scholarships)
    print(f"Finished downloading {len(htmls_of_scholarships)} pages.\n")

    print("Starting parsing of lists of scholarships...")
    list_of_all_scholarships = collect_all_scholarships(
        parse_all(htmls_of_scholarships, scholarships_list_parser))
    print(f"Found {len(list_of_all_scholarships)} scholarships.\n")

    store(list_of_all_scholarships, PARAMETERS['base_path'] / LINKS_FILENAME)


def get_all_scholarship_pages() -> None:
    links_with_scholarships = create_scholarship_links(
        PARAMETERS, LINKS_FILENAME)
    print(f"{len(links_with_scholarships)} scholarship pages to be downloaded.\n")

    print("Starting downloads for scholarship pages...")
    htmls_of_scholarships = run_all_async(links_with_scholarships)
    print(f"Finished downloading {len(htmls_of_scholarships)} pages.\n")

    print("Starting parsing of scholarship pages...")
    list_of_all_scholarships = parse_all(
        htmls_of_scholarships, scholarship_page_parser)
    print(f"Finished parsing {len(list_of_all_scholarships)} pages.\n")

    store(list_of_all_scholarships,
          PARAMETERS['base_path'] / SCHOLARSHIPS_FILENAME)


def convert_to_csv() -> None:
    print("Starting converting to csv...")

    with open(PARAMETERS['base_path'] / SCHOLARSHIPS_FILENAME, 'r') as scholarships_file, open(PARAMETERS['base_path'] / CSV_FILENAME, 'w', encoding="utf-8") as csv_file:
        scholarships = load(scholarships_file)
        headers = get_headers(scholarships)
        write_values(scholarships, csv_file, headers)

    print("Finished converting to csv.\n")


def main() -> None:
    setup(PARAMETERS)
    pull_scholarship_page_test()
    pull_list_page_test()
    get_list_of_scholarships()
    get_all_scholarship_pages()
    convert_to_csv()


if __name__ == '__main__':
    main()
