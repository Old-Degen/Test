from web3 import Web3, HTTPProvider
import csv
import os
from .nft_manager import NFTManager



class WalletManager:
    def __init__(self):
        self.web3 = Web3(HTTPProvider("https://mainnet.infura.io/v3/your-infura-project-id"))
        self.wallets = self.load_wallets_from_csv('private/wallets.csv')
        self.selected_wallet = self.get_wallet()
        self.nft_manager = NFTManager('http://localhost:8545')  # замените адрес на свой RPC-сервер

        # Загрузка кошельков из файла CSV
        wallets_path = os.path.join('private', 'wallets.csv')
        with open(wallets_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            self.wallets = [{'index': i, 'private_key': row[0]} for i, row in enumerate(reader)]


        # Убедитесь, что индекс кошелька в пределах допустимого диапазона
        if wallet_index >= len(private_keys):
            raise ValueError('Invalid wallet index')

        # Получение приватного ключа и создание аккаунта
        private_key = private_keys[wallet_index]
        self.account = self.web3.eth.account.from_key(private_key)

    def get_wallet_names(self):
        return [f"Wallet {wallet['index']}" for wallet in self.wallets]

    def distribute_tokens_and_nft(self, token_address, nft_address, amount, nft_id):
        # Получаем аккаунт, с которого будем отправлять токены
        from_account = self.web3.eth.account.from_key(self.selected_wallet['private_key'])
        nonce = self.web3.eth.get_transaction_count(from_account.address)

        # Получаем контракты ERC20 и NFT
        erc20_contract = self.web3.eth.contract(address=token_address, abi=ERC20_ABI)
        nft_contract = self.web3.eth.contract(address=nft_address, abi=NFT_ABI)

        # Для каждого кошелька в списке создаем транзакцию на отправку токенов и NFT
        for wallet in self.wallets:
            to_account = self.web3.eth.account.from_key(wallet['private_key'])

            # Отправляем токены
            tx = erc20_contract.functions.transfer(to_account.address, amount).buildTransaction({
                'from': from_account.address,
                'nonce': nonce,
            })
            signed_tx = from_account.sign_transaction(tx)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f"Tokens sent to {to_account.address}: {amount} (tx: {tx_hash.hex()})")
            nonce += 1

            # Отправляем NFT
            tx = nft_contract.functions.transferFrom(from_account.address, to_account.address, nft_id).buildTransaction(
                {
                    'from': from_account.address,
                    'nonce': nonce,
                })
            signed_tx = from_account.sign_transaction(tx)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f"NFT sent to {to_account.address}: {nft_id} (tx: {tx_hash.hex()})")
            nonce += 1

            # Обновляем данные кошелька в списке
            wallet_balance = erc20_contract.functions.balanceOf(to_account.address).call()
            wallet['balance'] = wallet_balance

            wallet_nft_balance = self.nft_manager.get_nft_balance(to_account.address, nft_address)
            wallet['nft_balance'] = wallet_nft_balance

            with open('private/wallets.csv', 'w', newline='') as csvfile:
                fieldnames = ['name', 'address', 'private_key', 'balance', 'nft_balance']
                writer = csv.DictWriter(csvfile, fieldnames=