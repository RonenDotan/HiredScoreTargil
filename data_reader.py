import json
import csv


def read_data(data, type):
    if type == "json":
        return json.loads(data)
    elif type == "csv":
        csv_reader = csv.DictReader(data.splitlines())
        return [row for row in csv_reader]
    else:
        raise Exception("Unsupported file type")
