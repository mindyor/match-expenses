import unicodecsv as csv


def load_csv(path):
    with open(path, mode="r") as csv_file:
        payload = list(csv.DictReader(csv_file, encoding='utf-8-sig'))
    return payload
