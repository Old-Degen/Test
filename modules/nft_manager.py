from typing import Any, Dict
from web3 import Web3

class NFTManager:
    def __init__(self, web3: Web3, wallet_manager: Any, nft_address: str, nft_abi: Dict[str, Any]):
        self.web3 = web3
        self.wallet_manager = wallet_manager
        self.nft_contract = self.web3.eth.contract(address=nft_address, abi=nft_abi)


    def get_nft_balance(self, address, contract_address):
        nft_contract = self.web3.eth.contract(address=contract_address, abi=NFT_ABI)
        return nft_contract.functions.balanceOf(address).call()

    def get_contract(self, contract_address, abi):
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        return contract
    # Другие методы для работы с контрактом NFT...

    def load_nft():
        # Load constants
        constants = Constants()

        # Get NFT contract address and ABI from constants
        nft_address = constants.NFT_CONTRACT_ADDRESS
        NFT_ABI = constants.NFT_ABI

        # Initialize Web3 and NFTManager
        web3 = Web3(HTTPProvider(constants.PROVIDER_URI))
        rpc = RPC(web3)
        nft_manager = NFTManager(nft_address, NFT_ABI, rpc)

        # Get WalletManager instance
        sender_address = constants.SENDER_ADDRESS
        wallet_manager = WalletManager(sender_address, web3)

        return nft_manager, wallet_manager