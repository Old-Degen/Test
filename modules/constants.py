# Импорты
from typing import Dict, Any

# Класс с константами
class Constants:
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
