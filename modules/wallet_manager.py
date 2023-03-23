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

    def get_wallets(self, chain: str, group: Optional[str] = None, name: Optional[str] = None) -> List[dict]:
        wallets = []
        for wallet in self.wallets:
            if wallet['chain'] == chain and (group is None or wallet['group'] == group) and (
                    name is None or wallet['name'] == name):
                wallets.append(wallet)
        return wallets[0] if name is not None else wallets

    def get_balances(self, chain: str, group: Optional[str] = None, name: Optional[str] = None) -> float:
        wallets = self.get_wallets(chain, group, name)
        if name is not None:
            return self.matic.balance_of(wallets['address'])
        else:
            balances = {}
            for wallet in wallets:
                balances[wallet['name']] = self.matic.balance_of(wallet['address'])
            return balances

    def send_tokens(self, chain: str, group: str, name: Optional[str] = None, to_address: str, amount: float) -> str:
        wallet = self.get_wallets(chain, group, name)

        # Initialize Matic object
        matic = Matic(matic_rpc_url=wallet['chain'], parent_chain_rpc=wallet['parent_chain_rpc'],
                      matic_wallet_private_key=wallet['private_key'])

        # Convert amount to wei
        amount_wei = int(amount * 10 ** 18)

        # Transfer tokens
        tx_hash = matic.transferTokens(to_address, amount_wei)

        return tx_hash
