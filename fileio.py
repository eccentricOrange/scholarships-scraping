
from json import dump, load
from pathlib import Path


def set_paths_and_dirs(provider: str) -> Path:
    base_dir_path = Path("data") / provider
    base_dir_path.mkdir(parents=True, exist_ok=True)

    return base_dir_path


def create_scholarship_links(parameters: dict, links_filename):
    with open(parameters['base_path'] / links_filename, 'r') as links_file:
        links_with_scholarships = load(links_file)

    return [scholarship['link'] for scholarship in links_with_scholarships]


def create_links_list(base_url: str, end: int, start=1) -> list:
    return [base_url.replace('*', str(i)) for i in range(start, end+1)]


def store(data: list, file_path: Path):
    with open(file_path, 'w') as file_object:
        dump(data, file_object, indent=4)
