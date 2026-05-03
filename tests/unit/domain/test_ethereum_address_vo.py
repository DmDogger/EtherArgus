import pytest

from domain.exceptions.exceptions import (
    InvalidEthereumAddressPrefix,
    InvalidEthereumLength,
)
from domain.value_objects.ethereum_address_vo import EthereumAddressValueObject


class TestEthereumAddressValueObject:
    def test_accepts_address_with_eth_mainnet_length_and_prefix(self) -> None:
        vo = EthereumAddressValueObject.create(
            address="0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97",
        )

        assert vo.wallet_address == "0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97"

    def test_rejects_address_when_byte_length_not_42_chars(self) -> None:
        with pytest.raises(InvalidEthereumLength):
            EthereumAddressValueObject.create(
                address="0x4838B106FCe9647Bdf1E7877BF73cE"
            )

    def test_rejects_address_when_missing_hex_prefix(self) -> None:
        wrong_prefix_42_chars = "1x" + "0" * 40

        with pytest.raises(InvalidEthereumAddressPrefix):
            EthereumAddressValueObject.create(address=wrong_prefix_42_chars)
