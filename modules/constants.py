# Импорты
from typing import Dict, Any
import json
import os

# Класс с константами
class Constants:
    def __init__(self):
        self.load_tokens()

    def load_tokens(self):
        nft_abi = {}
        token_abi = {}
        for file in os.listdir('ABI'):
            if file.endswith('.json'):
                with open(os.path.join('ABI', file), 'r') as f:
                    abi = json.load(f)
                if 'nft' in file:
                    nft_abi = abi
                elif 'token' in file:
                    token_abi = abi

        self.NFT_ABI = nft_abi
        self.TOKEN_ABI = token_abi

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
