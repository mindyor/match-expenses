import csv


def load_csv(path):
    with open(path, mode="r") as f:
        payload = list(csv.DictReader(f))
    return payload
