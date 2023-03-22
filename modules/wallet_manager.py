import csv
import os

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

    def distribute_tokens_and_nft(self, contract_address, abi, token_name, token_symbol, amount, recipient, nft_id):
        """
        Распределяет токены и NFT на заданный адрес.

        :param contract_address: Адрес контракта токена.
        :param abi: ABI контракта токена.
        :param token_name: Название токена.
        :param token_symbol: Символ токена.
        :param amount: Количество токенов для распределения.
        :param recipient: Адрес получателя.
        :param nft_id: ID NFT для распределения.
        """
        # Создаем экземпляр контракта токена
        token_contract = self.web3.eth.contract(address=contract_address, abi=abi)

        # Получаем основной кошелек и его приватный ключ
        main_wallet_address, main_wallet_private_key = self.get_wallet()

        # Подписываем транзакцию с помощью приватного ключа
        nonce = self.web3.eth.getTransactionCount(main_wallet_address)
        tx = {
            'nonce': nonce,
            'to': contract_address,
            'value': 0,
            'gas': 2000000,
            'gasPrice': self.web3.eth.gasPrice,
            'data':
                token_contract.functions.transfer(recipient, amount).buildTransaction({'from': main_wallet_address})[
                    'data']
        }
        signed_tx = self.web3.eth.account.signTransaction(tx, main_wallet_private_key)

        # Отправляем транзакцию на сеть
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Ожидаем подтверждения транзакции
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

        # Проверяем статус транзакции
        if tx_receipt['status'] == 0:
            print("Transaction failed.")
            return

        # Создаем экземпляр контракта NFT
        nft_contract = self.nft_manager.get_contract_by_name(token_name)

        # Получаем основной кошелек и его приватный ключ
        main_wallet_address, main_wallet_private_key = self.get_wallet()

        # Подписываем транзакцию с помощью приватного ключа
        nonce = self.web3.eth.getTransactionCount(main_wallet_address)
        tx = {
            'nonce': nonce,
            'to': nft_contract.address,
            'value': 0,
            'gas': 2000000,
            'gasPrice': self.web3.eth.gasPrice,
            'data': nft_contract.functions.safeTransferFrom(main_wallet_address, recipient, nft_id).buildTransaction(
                {'from': main_wallet_address})['data']
        }
        signed_tx = self.web3.eth.account.signTransaction(tx, main_wallet_private_key)

        # Отправляем транзакцию на сеть
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Ожидаем подтверждения транзакции
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

        # Проверяем статус транзакции
        if tx_receipt['status'] == 0:
