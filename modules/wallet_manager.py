import os
import csv
import random
import string
from web3 import Web3, HTTPProvider
from modules.rpc import get_rpc
from modules.nft_manager import NFTManager



class WalletManager:
    def __init__(self):
        # Инициализация web3
        self.web3 = Web3(HTTPProvider(get_rpc()[0]))
        # Загрузка кошельков из файла
        self.wallets = self.load_wallets_from_csv('private/wallets.csv')
        # Инициализация NFT-менеджера
        self.nft_manager = NFTManager(get_rpc()[0])

    def load_wallets_from_csv(self, filename):
        """
        Load a list of wallets from a CSV file.

        Args:
            filename (str): The name of the CSV file to load.

        Returns:
            list: A list of wallets, where each wallet is a dictionary containing the fields
            "chain", "group", "name", "address", and "private_key".

        """
        # Check if the file exists, and create it if it doesn't
        if not os.path.isfile(filename):
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['chain', 'group', 'name', 'address', 'private_key']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

        # Load the wallets from the CSV file
        wallets = []
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                wallets.append({
                    'chain': row['chain'],
                    'group': row['group'],
                    'name': row['name'],
                    'address': row['address'],
                    'private_key': row['private_key']
                })
        return wallets

    def get_wallet(self):
        # Получение списка кошельков из объекта класса WalletManager
        wallets = self.wallets

        # Если список кошельков пустой, выводим сообщение об ошибке
        if not wallets:
            print('Error: No wallets found!')
            return None

        # Иначе выводим список кошельков и предлагаем пользователю выбрать номер кошелька
        print('Available wallets:')
        for i, wallet in enumerate(wallets):
            print(f"{i + 1}. {wallet['name']}")
        while True:
            try:
                choice = int(input('Select a wallet number: '))
                # Если выбранный номер не соответствует ни одному из кошельков, выводим сообщение об ошибке
                if choice < 1 or choice > len(wallets):
                    print('Invalid choice, try again!')
                    continue
                break
            # Если пользователь вводит не число, выводим сообщение об ошибке
            except ValueError:
                print('Invalid choice, try again!')
                continue
        # Возвращаем выбранный кошелек
        return wallets[choice - 1]

    def generate_wallet(self, group, prefix):
        # Создание нового кошелька
        pass

    def get_wallets_by_group_and_prefix(self, group, prefix):
        # Получение списка кошельков по группе и префиксу
        pass

    def save_wallets_to_csv(self, filename):
        # Сохранение списка кошельков в CSV-файл
        pass

    def get_balance(self):
        # Получение баланса текущего кошелька
        pass

    def transfer_eth(self, to_address, value):
        # Отправка эфира со текущего кошелька
        pass

    def get_token_balance(self, contract_address):
        # Получение баланса токенов
        pass

    def transfer_tokens(self, contract_address, to_address, value):
        # Отправка токенов
        pass

    def create_nft(self, contract_address, token_id, metadata_url):
        # Создание нового NFT
        pass

    def get_nft(self, contract_address, token_id):
        # Получение информации о NFT
        pass

    def get_nfts_by_owner(self, owner_address):
        # Получение списка NFT, принадлежащих владельцу
        pass

    def transfer_nft(self, contract_address, token_id, to_address):
        # Передача NFT
        pass

    def burn_nft(self, contract_address, token_id):
        # Уничтожение NFT
        pass
