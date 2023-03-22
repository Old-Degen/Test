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

    def distribute_tokens_and_nft(self, token_address: str, token_abi: str, nft_address: str, nft_abi: str, group: str,
                                  prefix: str):
        """
        Раздает токены и NFT в кошельки из определенной группы с определенным префиксом.

        :param token_address: Адрес контракта токена
        :param token_abi: ABI контракта токена
        :param nft_address: Адрес контракта NFT
        :param nft_abi: ABI контракта NFT
        :param group: Группа кошельков, в которую будут раздаваться токены и NFT
        :param prefix: Префикс кошельков, в которые будут раздаваться токены и NFT
        """
        # Получаем список кошельков, соответствующих заданным параметрам группы и префикса
        wallets = self.get_wallets_by_group_and_prefix(group, prefix)

        # Подключаемся к RPC-серверу, используя первый адрес из списка доступных
        web3 = Web3(HTTPProvider(get_rpc()[0]))

        # Загружаем контракты токена и NFT
        token_contract = web3.eth.contract(address=web3.toChecksumAddress(token_address), abi=json.loads(token_abi))
        nft_contract = web3.eth.contract(address=web3.toChecksumAddress(nft_address), abi=json.loads(nft_abi))

        # Запрашиваем у пользователя количество токенов для раздачи и проверяем, что это число больше 0
        token_amount = input_with_int_check("Enter the amount of tokens to distribute: ", min_value=1)

        # Запрашиваем у пользователя ID NFT для раздачи и проверяем, что это число больше 0
        nft_id = input_with_int_check("Enter the ID of the NFT to distribute: ", min_value=1)

        # Перебираем все кошельки и раздаем им токены и NFT
        for wallet in wallets:
            # Получаем адрес кошелька в формате, пригодном для использования в контрактах
            wallet_address = web3.toChecksumAddress(wallet["address"])

            # Проверяем, что кошелек не пустой
            balance = token_contract.functions.balanceOf(wallet_address).call()
            if balance == 0:
                continue

            # Раздаем токены
            transaction = token_contract.functions.transfer(wallet_address, token_amount).buildTransaction({
                "from": self.account.address,
                "nonce": web3.eth.getTransactionCount(self.account.address),
                "gas": 200000,
                "gasPrice": web3.toWei('50', 'gwei')
            })
            signed_txn = self.account.sign_transaction(transaction)
            tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            print(f"Tokens sent to {wallet_address}: {token_amount} (tx: {web3.toHex(tx_hash)})")

            # Раздаем NFT
            transaction
