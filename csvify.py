from csv import DictWriter
from io import TextIOWrapper

def get_headers(file: dict):
    headers = set()

    for scholarship in file:
        for key in scholarship:
            headers.add(key)

    return list(headers)


def write_values(json_file: dict, csv_file: TextIOWrapper, headers: list):
    writer = DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(json_file)