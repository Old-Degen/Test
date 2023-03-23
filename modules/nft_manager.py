from web3 import Web3, HTTPProvider



class NFTManager:
    def __init__(self, rpc_url):
        self.web3 = Web3(HTTPProvider(rpc_url))

    def get_nft_balance(self, address, contract_address):
        nft_contract = self.web3.eth.contract(address=contract_address, abi=NFT_ABI)
        return nft_contract.functions.balanceOf(address).call()

    # Другие методы для работы с контрактом NFT...
