from typing import List, Optional, Tuple

import csv
import os
from matic import Matic
from web3 import Web3


class WalletManager:
    def __init__(self, contracts_path: str = 'contracts', wallets_path: str = 'wallets.csv'):
        self.contracts_path = contracts_path
        self.wallets_path = wallets_path
        self.wallets = self.load_wallets()
        self.contract_addresses = contract_addresses
        self.matic = Matic(chainId=137, api_url="https://rpc-mainnet.maticvigil.com/")
        self.matic = Matic(chainId=137, api_url="https://rpc-mainnet.maticvigil.com/")
        self.wallets = []
        self.import_wallets_from_csv()

    def load_wallets(self) -> List[dict]:
        wallets = []
        if os.path.exists(self.wallets_path):
            with open(self.wallets_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    wallets.append(row)
        return wallets

    def create_account(self, chain: str, group: str, name: str) -> Tuple[str, str]:
        account = self.matic.account.create()
        private_key = account.privateKey
        address = account.address
        return address, private_key

    def import_wallets_from_csv(self):
        with open('wallets.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.wallets.append(row)

    def import_account(self, chain: str, group: str, name: str, private_key: str, address: str) -> None:
        pass

    def get_balance(self, chain: str, group: str, name: Optional[str] = None) -> float:
        pass

    def send_tokens(self, chain: str, group: str, name: Optional[str] = None, to_address: str, amount: float) -> str:
        pass
