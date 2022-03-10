from csv import DictWriter
from io import TextIOWrapper
from json import dump, load
from pathlib import Path


def create_scholarship_links(parameters: dict, links_filename) -> list:
    with open(parameters['base_path'] / links_filename, 'r') as links_file:
        links_with_scholarships = load(links_file)

    return [scholarship['link'] for scholarship in links_with_scholarships]


def setup(parameters: dict) -> None:
    base_dir_path = Path("data") / str(parameters['provider_name'])
    base_dir_path.mkdir(parents=True, exist_ok=True)
    parameters['base_path'] = base_dir_path


def create_links_list(base_url: str, end: int, start=1) -> list:
    return [base_url.replace('*', str(i)) for i in range(start, end+1)]


def store(data: list, file_path: Path) -> None:
    with open(file_path, 'w') as file_object:
        dump(data, file_object, indent=4)


def get_headers(file: dict) -> list:
    headers = set()

    for scholarship in file:
        for key in scholarship:
            headers.add(key)

    return ['id'] + ['select'] + list(headers)


def write_values(json_file: dict, csv_file: TextIOWrapper, headers: list) -> None:
    writer = DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(json_file)
