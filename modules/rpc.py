from web3 import Web3


class RPC:
    def __init__(self, provider_uri):
        self.provider_uri = provider_uri
        self.w3 = Web3(Web3.HTTPProvider(self.provider_uri))

    def get_block_number(self):
        return self.w3.eth.block_number
