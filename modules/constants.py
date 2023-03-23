import os
import json

ABIS_DIR = 'ABI'

class Constants:
    def __init__(self):
        self.load_tokens()
        self.load_nft()
        self.Polygon_NFT_CONTRACT_ADDRESS = "0x3816BEEa5A6DD8D2A8cf0515Ba555FeF16714a10"
        self.MATIC_CONTRACT_ADDRESS = "0x0000000000000000000000000000000000001010"

    def load_tokens(self):
        self.TOKEN_ABI = None
        for filename in os.listdir(ABIS_DIR):
            if filename.endswith(".json"):
                with open(os.path.join(ABIS_DIR, filename)) as f:
                    data = json.load(f)
                    if filename[:-5] == 'matic':
                        self.TOKEN_ABI = data

    def load_nft(self):
        self.NFT_ABI = None
        for filename in os.listdir(ABIS_DIR):
            if filename.endswith(".json"):
                with open(os.path.join(ABIS_DIR, filename)) as f:
                    data = json.load(f)
                    if filename[:-5] == 'Polygon_NFT':
                        self.NFT_ABI = data
