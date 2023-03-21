import csv
import os


def get_rpc(group='Polygon'):
    filename = os.path.join(os.path.dirname(__file__), '..', 'private', 'rpc_list.csv')
    rpc_list = []

    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row['group'] == group:
                rpc_list.append(row['uri'])

    return rpc_list
