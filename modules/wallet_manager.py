from web3 import Web3
import eth_utils
from web3.auto import w3
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
from modules.settings import PROVIDER_URI, RPC_URI


class WalletManager:
    def __init__(self, provider_uri=PROVIDER_URI, rpc_uri=RPC_URI):
        self.web3 = Web3(Web3.HTTPProvider(provider_uri))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.web3.eth.setGasPriceStrategy(medium_gas_price_strategy)
        self.account = self.web3.eth.account.privateKeyToAccount(private_key)
        self.utils = Utils()

    def get_balance(self, address):
        return self.web3.eth.get_balance(address)

    def get_token_balance(self, address, contract_address, decimals):
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        balance = contract.functions.balanceOf(address).call()
        return balance / 10 ** decimals

    def transfer(self, to_address, value):
        gas = self.web3.eth.estimateGas({'from': self.account.address, 'to': to_address, 'value': value})
        tx = {'from': self.account.address, 'to': to_address, 'value': value, 'gas': gas}
        signed_tx = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return self.web3.toHex(tx_hash)

    def transfer_token(self, to_address, contract_address, value, decimals):
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        token_amount = value * 10 ** decimals
        gas = contract.functions.transfer(to_address, token_amount).estimateGas({'from': self.account.address})
        tx = contract.functions.transfer(to_address, token_amount).buildTransaction({
            'from': self.account.address,
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
            'gas': gas,
            'gasPrice': self.web3.eth.gas_price,
            'chainId': self.web3.eth.chain_id
        })
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.account.privateKey)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.web3.toHex(tx_hash)

    def generate_wallets(self, group, name, count):
        for i in range(count):
            private_key = eth_utils.keccak(hexstr=str(w3.eth.generate_private_key())).hex()
            address = w3.eth.account.from_key(private_key).address
            self.utils.add_to_csv(group, f"{name}_{i}", address, private_key)
        return count

    @staticmethod
    def add_to_csv(group, name, address, private_key):
        import csv
        import os
        filename = os.path.join(os.path.dirname(__file__), 'private', 'wallets.csv')
        file_exists = os.path.isfile(filename)

        with open(filename, 'a', newline='') as csvfile:
            headers = ['Group', 'Name', 'Address', 'Private Key']
            writer = csv.DictWriter(csvfile, fieldnames=headers)

            if not file_exists:
                writer.writeheader()

            writer.writerow({'Group': group, 'Name': name, 'Address': address, 'Private Key': private_key})
