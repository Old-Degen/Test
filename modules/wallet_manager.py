import os
import csv
import random
import string
from web3 import Web3
from web3.providers.rpc import HTTPProvider
from modules.rpc import get_rpc



class WalletManager:
    def __init__(self):
        self.web3 = Web3(HTTPProvider(get_rpc()[0]))
        self.wallets = self.load_wallets_from_csv('private/wallets.csv')
        self.selected_wallet = self.get_wallet()
        self.nft_manager = NFTManager(get_rpc()[0])

    def load_wallets_from_csv(self, filename):
        if not os.path.isfile(filename):
            return []
        wallets = []
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                wallets.append({
                    'group': row['group'],
                    'prefix': row['prefix'],
                    'address': row['address'],
                    'private_key': row['private_key']
                })
        return wallets

    def get_wallet(self):
        """
        Запрашивает у пользователя выбор основного кошелька и возвращает его адрес и приватный ключ.

        :return: Кортеж, содержащий адрес и приватный ключ выбранного кошелька.
        """
        # Выводим список кошельков и запрашиваем у пользователя выбор
        print("Select main wallet:")
        for i, wallet in enumerate(self.wallets):
            print(f"{i}. {wallet['name']}")
        wallet_index = input_with_int_check("Enter the index of the wallet to select: ",
                                            max_value=len(self.wallets) - 1)

        # Возвращаем адрес и приватный ключ выбранного кошелька
        wallet = self.wallets[wallet_index]
        return wallet['address'], wallet['private_key']

    def generate_wallet(self):
        """
        Генерирует новый кошелек и сохраняет его в CSV-файл.

        :return: Кортеж, содержащий адрес и приватный ключ нового кошелька.
        """
        # Генерируем новый кошелек
        account = self.web3.eth.account.create()

        # Сохраняем его в CSV-файл
        with open('private/wallets.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(['', account.address, account.privateKey.hex()])

        # Возвращаем адрес и приватный ключ нового кошелька
        return account.address, account.privateKey.hex()

    def get_wallets_by_group_and_prefix(self, group, prefix):
        """
        Возвращает список кошельков из заданной группы с заданным префиксом.

        :param group: Группа кошельков.
        :param prefix: Префикс кошельков.
        :return: Список кортежей, каждый из которых содержит адрес и приватный ключ кошелька.
        """
        wallets = []
        for wallet in self.wallets:
            if wallet['group'] == group and wallet['name'].startswith(prefix):
                wallets.append((wallet['address'], wallet['private_key']))
        return wallets

    def distribute_tokens_and_nft(self, token_address, token_abi, nft_contract_address, nft_abi, recipients):
        token_contract = self.web3.eth.contract(address=token_address, abi=token_abi)
        nft_contract = self.web3.eth.contract(address=nft_contract_address, abi=nft_abi)

        for recipient in recipients:
            wallet = recipient['wallet']
            amount = recipient['amount']
            nft_token_id = recipient.get('nft_token_id')
            if nft_token_id is None:
                nft_token_id = 0

            nonce = self.web3.eth.get_transaction_count(self.selected_wallet['address'])
            gas_price = self.web3.eth.gas_price
            gas_limit = 250000

            # Transfer token
            tx = token_contract.functions.transfer(wallet, amount).buildTransaction({
                'chainId': 1,
                'gas': gas_limit,
                'gasPrice': gas_price,
                'nonce': nonce,
            })
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.selected_wallet['private_key'])
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

            if tx_receipt['status'] == 0:
                print(f"Transfer failed for {wallet}")
                continue

            # Mint NFT
            if nft_token_id != 0:
                tx = nft_contract.functions.mint(wallet, nft_token_id).buildTransaction({
                    'chainId': 1,
                    'gas': gas_limit,
                    'gasPrice': gas_price,
                    'nonce': nonce + 1,
                })
                signed_tx = self.web3.eth.account.sign_transaction(tx, self.selected_wallet['private_key'])
                tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

                if tx_receipt['status'] == 0:
                    print(f"Minting NFT failed for {wallet}")
                    continue

            print(f"Successfully distributed {amount} tokens and minted NFT with id {nft_token_id} to {wallet}")
