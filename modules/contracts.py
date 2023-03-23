import json
from web3 import Web3
from web3.eth.contract import Contract


class Contracts:
    def __init__(self, web3: Web3):
        self.web3 = web3

    def get_contract(self, address: str, abi_path: str) -> Contract:

        with open(abi_path) as f:
            abi = json.load(f)

        return self.web3.eth.contract.Contract(address=address, abi=abi)


ERC721_CONTRACTS = {
    '0x0': [
        {
            'constant': True,
            'inputs': [{'name': '_tokenId', 'type': 'uint256'}],
            'name': 'getApproved',
            'outputs': [{'name': '', 'type': 'address'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': False,
            'inputs': [{'name': '_to', 'type': 'address'}, {'name': '_tokenId', 'type': 'uint256'}],
            'name': 'transferFrom',
            'outputs': [],
            'payable': False,
            'stateMutability': 'nonpayable',
            'type': 'function'
        },
        # Другие методы контракта ERC-721
    ],
    '0x1': [
        # ABI для другого контракта ERC-721
    ],
    # Другие контракты ERC-721
}
