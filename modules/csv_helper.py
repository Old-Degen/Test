import csv
import os

def add_to_csv(group, name, address, private_key):
    filename = os.path.join(os.path.dirname(__file__), '..', 'private', 'wallets.csv')
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as csvfile:
        headers = ['Group', 'Name', 'Address', 'Private Key']
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        if not file_exists:
            writer.writeheader()

        writer.writerow({'Group': group, 'Name': name, 'Address': address, 'Private Key': private_key})
