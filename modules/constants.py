
from typing import Dict, Any
import json

# Класс с константами
class Constants:
    def __init__(self):
        self.load_tokens()

    def load_tokens(self):
        with open('ABI/matic.json', 'r') as f:
            self.TOKEN_ABI = json.load(f)




    # Адреса смарт-контрактов
    NFT_CONTRACT_ADDRESS = "0x1234567890abcdef"
    TOKEN_CONTRACT_ADDRESS = "0xfedcba0987654321"

    # ABI для смарт-контрактов
    NFT_ABI: Dict[str, Any] = {...}
    TOKEN_ABI: Dict[str, Any] = {...}

    # Максимальное количество NFT, которое можно создать
    MAX_NFT_COUNT = 1000000

    # Другие константы
    SOME_CONSTANT = "some_value"

    # Методы класса Constants (если необходимо)
    @classmethod
    def get_some_value(cls) -> str:
        return cls.SOME_CONSTANT

    with open('ABI/matic.json', 'r') as f:
        TOKEN_ABI = json.load(f)

    TOKEN_CONTRACT_ADDRESS = "0xfedcba0987654321"
