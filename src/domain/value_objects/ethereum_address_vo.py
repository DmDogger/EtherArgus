from dataclasses import dataclass
from typing import final

from domain.exceptions.exceptions import (
    InvalidEthereumLength,
    InvalidEthereumAddressPrefix,
)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class EthereumAddressValueObject:
    wallet_address: str

    def __post_init__(self):
        if len(self.wallet_address) != 42:
            raise InvalidEthereumLength(
                f"Wallet address should contain only 42 chars, but got: {self.wallet_address}"
            )

        if not self.wallet_address.startswith("0x"):
            raise InvalidEthereumAddressPrefix(
                f"Wallet address should start with '0x', but starts with: {self.wallet_address[:1]}"
            )

    @classmethod
    def create(cls, *, address: str) -> "EthereumAddressValueObject":
        return cls(wallet_address=address)
