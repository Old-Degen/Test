import os
import json

ABIS_DIR = 'ABI'

class Constants:
    def __init__(self):
        self.load_tokens()

    def load_tokens(self):
        self.NFT_ABI = None
        self.TOKEN_ABI = None
        for filename in os.listdir(ABIS_DIR):
            if filename.endswith(".json"):
                with open(os.path.join(ABIS_DIR, filename)) as f:
                    data = json.load(f)
                    if filename[:-5] == 'Polygon_NFT':
                        self.NFT_ABI = data
                    elif filename[:-5] == 'matic':
                        self.TOKEN_ABI = data
