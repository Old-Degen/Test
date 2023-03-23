import os
import csv
import random
import string
from web3 import Web3, HTTPProvider
from modules.rpc import RPC
from modules.nft_manager import NFTManager
from eth_utils import to_wei
from modules.constants import NFT_ABI




class WalletManager:
    def __init__(self):
        # Инициализация web3
        self.rpc = RPC("Polygon")
        self.web3 = Web3(HTTPProvider(self.rpc.uri))
        # Загрузка кошельков из файла
        self.wallets = self.load_wallets_from_csv(os.path.join('private', 'wallets.csv'))
        # Инициализация NFT-менеджера
        self.nft_manager = NFTManager(self.rpc.uri)
        self.w3 = Web3(HTTPProvider(self.rpc.uri))
        self.private_key = self.wallets[0]['private_key']
        self.account = self.web3.eth.account.from_key(self.private_key)
        self.address = self.account.address

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
        return wallets

    def generate_wallet(self, group, name):
        # Создание нового кошелька
        # Генерация ключей
        w3 = Web3()
        acct = w3.eth.account.create()
        private_key = acct.privateKey.hex()
        public_key = acct.publicKey.hex()
        address = acct.address

        # Добавление кошелька в список
        chain = 'Polygon' # пока что только для Polygon
        row = {'chain': chain, 'group': group, 'name': f"{name}_{len(self.wallets)+1}",
               'address': address, 'private_key': private_key}
        self.wallets.append(row)

        # Запись в файл
        filename = 'private/wallets.csv'
        file_exists = os.path.isfile(filename)
        with open(filename, mode='a', newline='') as csv_file:
            fieldnames = ['chain', 'group', 'name', 'address', 'private_key']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow(row)
        return row

    def get_wallets_by_group_and_name(self, group, name):
        # Получение списка кошельков по группе и названию
        filtered_wallets = [w for w in self.wallets if w.group == group and w.name == name]
        return filtered_wallets

    def save_wallets_to_csv(self, filename):
        # Сохранение списка кошельков в CSV-файл
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['chain', 'group', 'name', 'address', 'private_key']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for wallet in self.wallets:
                writer.writerow({
                    'chain': wallet['chain'],
                    'group': wallet['group'],
                    'name': wallet['name'],
                    'address': wallet['address'],
                    'private_key': wallet['private_key']
                })


    def get_balance(self, address, token_address):
        # Получение баланса токенов Matic на блокчейне Polygon
        contract_address = self.web3.to_checksum_address(token_address)
        abi = [{"constant": True, "inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"}]
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        balance = contract.functions.balanceOf(address).call()
        return balance

    def transfer_matic(self, to_address, value):
        # Отправка MATIC со текущего кошелька
        nonce = self.w3.eth.get_transaction_count(self.address)
        gas_price = to_wei('5', 'gwei')
        tx = {
            'nonce': nonce,
            'to': to_address,
            'value': value,
            'gas': 21000,
            'gasPrice': gas_price,
        }
        signed_tx = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    def get_token_balance(self, contract_address):
        # Получение баланса токенов
        ABI = [{"constant": True, "inputs": [{"name": "owner", "type": "address"}], "name": "balanceOf",
                "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view",
                "type": "function"}]
        contract = self.web3.eth.contract(address=contract_address, abi=ABI)
        balance = contract.functions.balanceOf(self.address).call()
        return balance

    def transfer_tokens(self, contract_address, to_address, value):
        ABI = [{"constant": True, "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
                "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "payable": False, "stateMutability": "view", "type": "function"}]
        # Получаем экземпляр контракта
        contract = self.web3.eth.contract(address=contract_address, abi=ABI)
        # Получаем количество токенов на кошельке отправителя
        token_balance = contract.functions.balanceOf(self.address).call()
        # Проверяем, что у отправителя достаточно токенов для перевода
        if token_balance < value:
            print(f"Not enough tokens to transfer. Current balance: {token_balance}")
            return None
        # Получаем количество десятичных знаков токена
        decimals = contract.functions.decimals().call()
        # Конвертируем количество токенов в единицы учета токена (например, для ERC20 - в wei)
        token_value = value * 10 ** decimals
        # Подготавливаем данные для отправки транзакции
        tx_data = contract.functions.transfer(to_address, token_value).buildTransaction({
            'nonce': self.w3.eth.get_transaction_count(self.address),
            'gas': 100000,
            'gasPrice': self.w3.eth.gas_price
        })
        # Подписываем транзакцию и отправляем на сеть
        signed_tx = self.account.sign_transaction(tx_data)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    def get_nft(self, contract_address, token_id):
        nft_contract = self.nft_manager.get_contract(contract_address, NFT_ABI)
        return nft_contract.functions.tokenURI(token_id).call()

    def get_nfts_by_owner(self, owner_address):
        # Создаем пустой список для хранения NFT, принадлежащих владельцу
        nfts_by_owner = []

        # Проходим по всем NFT в списке self.nfts
        for nft in self.nfts:
            # Проверяем, совпадает ли owner_address с адресом владельца NFT
            if nft.owner == owner_address:
                # Если да, добавляем NFT в список nfts_by_owner
                nfts_by_owner.append(nft)

        # Возвращаем список NFT, принадлежащих владельцу
        return nfts_by_owner

    def transfer_nft(self, contract_address, token_id, to_address):
        # Находим NFT в списке self.nfts
        for nft in self.nfts:
            if nft.contract_address == contract_address and nft.token_id == token_id:
                # Проверяем, что адрес отправителя NFT совпадает с адресом владельца NFT
                if nft.owner == self.sender_address:
                    # Обновляем адрес владельца на to_address
                    nft.owner = to_address
                    return True
                else:
                    return False
        # Если NFT не найден в списке self.nfts, возвращаем False
        return False

    success = wallet_manager.transfer_nft("0xcontract", "123", "0xrecipient")
    if success:
        print("NFT successfully transfered")
    else:
        print("Failed transferring NFT")

    def burn_nft(self, contract_address, token_id):
        # Уничтожение NFT
        pass
