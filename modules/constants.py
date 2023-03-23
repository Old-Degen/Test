import json
import os

ABIS_DIR = 'ABI'

abis = {}
for filename in os.listdir(ABIS_DIR):
    if filename.endswith('.json'):
        with open(os.path.join(ABIS_DIR, filename), 'r') as f:
            abis[filename[:-5]] = json.load(f)

class Constants:
    def __init__(self):
        self.load_tokens()

    def load_tokens(self):
        self.NFT_ABI = abis['nft']
        self.TOKEN_ABI = abis['token']

    # Адреса смарт-контрактов
    NFT_CONTRACT_ADDRESS = "0x1234567890abcdef"
    TOKEN_CONTRACT_ADDRESS = "0xfedcba0987654321"

    # Максимальное количество NFT, которое можно создать
    MAX_NFT_COUNT = 1000000

    # Другие константы
    SOME_CONSTANT = "some_value"

    # Методы класса Constants (если необходимо)
    @classmethod
    def get_some_value(cls) -> str:
        return cls.SOME_CONSTANT
