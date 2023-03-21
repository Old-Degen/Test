import eth_utils
import string
import os
import csv
import random
from web3.auto import w3

class WalletManager:
    def __init__(self, provider_uri, private_key):
        self.web3 = Web3(Web3.HTTPProvider(provider_uri))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.web3.eth.setGasPriceStrategy(medium_gas_price_strategy)
        self.account = self.web3.eth.account.privateKeyToAccount(private_key)

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

    def generate_wallets(self, group, name, number_of_wallets):
        wallets = []
        for i in range(number_of_wallets):
            private_key = eth_utils.keccak(hexstr=str(w3.eth.generate_private_key())).hex()
            address = w3.eth.account.from_key(private_key).address
            self.add_to_csv(group, name, address, private_key)
            wallets.append((address, private_key))
        return wallets

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
    def generate_random_number():
        return random.randint(0, 100)

    @staticmethod
    def generate_random_string(length=8):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in
