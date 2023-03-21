import csv

def add_to_csv(filename, group, name, address, private_key):
    file_exists = csv_file_exists(filename)

    with open(filename, 'a', newline='') as csvfile:
        headers = ['Group', 'Name', 'Address', 'Private Key']
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        if not file_exists:
            writer.writeheader()

        writer.writerow({'Group': group, 'Name': name, 'Address': address, 'Private Key': private_key})

def csv_file_exists(filename):
    return os.path.isfile(filename)
