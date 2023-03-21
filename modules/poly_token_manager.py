from web3 import Web3

class PolyTokenManager:
    def __init__(self, web3: Web3, contract_address: str):
        self.web3 = web3
        self.contract_address = contract_address
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self._get_contract_abi())

    def _get_contract_abi(self):
        abi = [
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "token",
                        "type": "address"
                    },
                    {
                        "internalType": "bool",
                        "name": "_isNative",
                        "type": "bool"
                    }
                ],
                "name": "addToken",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
        return abi

    def add_token(self, token_address: str):
        self.contract.functions.addToken(token_address, True).transact({'from': self.web3.eth.defaultAccount})
