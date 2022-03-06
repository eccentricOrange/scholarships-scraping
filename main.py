from json import load
from pull import pull_test_page, parse_all, run_all_async
from fileio import create_links_list, set_paths_and_dirs, create_scholarship_links, store
from data.template.parsers import parameters, scholarships_list_parser, scholarship_page_parser, TEST_PAGE_FILENAME, TEST_PAGE_LIST_FILENAME
from csvify import get_headers, write_values

LINKS_FILENAME = 'links.json'
SCHOLARSHIPS_FILENAME = 'scholarships.json'
CSV_FILENAME = 'scholarships.csv'


def collect_all_scholarships(lists_of_lists: list):
    scholarships = []

    for list_of_scholarships in lists_of_lists:
        scholarships.extend(list_of_scholarships)

    return scholarships


def setup():
    parameters['base_path'] = set_paths_and_dirs(parameters['provider_name'])


def pull_scholarship_page_test():
    pull_test_page(parameters['page_link'],
                   parameters['base_path'], TEST_PAGE_FILENAME)


def pull_list_page_test():
    pull_test_page(parameters['base_url'].replace(
        '*', str(1)), parameters['base_path'], TEST_PAGE_LIST_FILENAME)


def get_list_of_scholarships():
    links_with_scholarships = create_links_list(
        parameters['base_url'], parameters['end'], parameters['start'])
    print("Starting downloads for lists of scholarships...")
    htmls_of_scholarships = run_all_async(links_with_scholarships)
    print("Finished downloads for lists of scholarships.\n")
    print("Starting parsing of lists of scholarships...")
    list_of_all_scholarships = collect_all_scholarships(
        parse_all(htmls_of_scholarships, scholarships_list_parser))
    print("Finished parsing of lists of scholarships.\n")
    store(list_of_all_scholarships, parameters['base_path'] / LINKS_FILENAME)


def get_all_scholarship_pages():
    links_with_scholarships = create_scholarship_links(
        parameters, LINKS_FILENAME)
    print("Starting downloads for scholarship pages...")
    htmls_of_scholarships = run_all_async(links_with_scholarships)
    print("Finished downloads for scholarship pages.\n")
    print("Starting parsing of scholarship pages...")
    list_of_all_scholarships = parse_all(
        htmls_of_scholarships, scholarship_page_parser)
    print("Finished parsing of scholarship pages.\n")
    store(list_of_all_scholarships,
          parameters['base_path'] / SCHOLARSHIPS_FILENAME)


def convert_to_csv():
    print("Starting converting to csv...")
    with open(parameters['base_path'] / SCHOLARSHIPS_FILENAME, 'r') as scholarships_file, open(parameters['base_path'] / CSV_FILENAME, 'w', encoding="utf-8") as csv_file:
        scholarships = load(scholarships_file)
        headers = get_headers(scholarships)
        write_values(scholarships, csv_file, headers)

    print("Finished converting to csv.\n")


if __name__ == '__main__':
    setup()
    pull_scholarship_page_test()
    pull_list_page_test()
    get_list_of_scholarships()
    get_all_scholarship_pages()
    convert_to_csv()
