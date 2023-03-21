import csv
import os

class Utils:
    @staticmethod
    def add_to_csv(group, name, address, private_key):
        filename = os.path.join(os.path.dirname(__file__), 'private', 'wallets.csv')
        file_exists = os.path.isfile(filename)

        with open(filename, 'a', newline='') as csvfile:
            headers = ['Group', 'Name', 'Address', 'Private Key']
            writer = csv.DictWriter(csvfile, fieldnames=headers)

            if not file_exists:
                writer.writeheader()

            writer.writerow({'Group': group, 'Name': name, 'Address': address, 'Private Key': private_key})

    @staticmethod
    def private_key_to_public_key(private_key):
        # Код для преобразования приватного ключа в публичный ключ
        pass

    @staticmethod
    def is_valid_address(address):
        # Код для проверки корректности адреса криптовалюты
        pass
