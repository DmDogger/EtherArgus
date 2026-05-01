from collections.abc import Sequence
from decimal import Decimal
from typing import Self

from infrastructure.etherscan_fetcher.schemas.etherscan_schemas import (
    TokenTransfersSchema,
)
from infrastructure.feature_extractor.enums import FeaturesEnum


class TokenTransfersFeatureBuilder:
    """Builds aggregate features from ERC-20 token transfers."""

    _features: dict[FeaturesEnum, int | Decimal | float]

    def __init__(self, address: str, transfers: Sequence[TokenTransfersSchema]):
        self._address = address
        self._transfers = tuple(transfers)
        self._sent = tuple(
            (tx, self._scaled_amount(tx))
            for tx in transfers
            if tx.from_address == address
        )
        self._received = tuple(
            (tx, self._scaled_amount(tx))
            for tx in transfers
            if tx.to_address == address
        )
        self._features = {}

    @staticmethod
    def _scaled_amount(tx: TokenTransfersSchema) -> Decimal:
        """Converts raw token value using token decimals."""

        return Decimal(tx.value) / (Decimal(10) ** tx.token_decimal)

    def total_erc20_tnx(self) -> Self:
        """Adds the total number of ERC-20 transfers."""

        self._features[FeaturesEnum.TOTAL_ERC20_TNX] = len(self._transfers)
        return self

    def erc20_total_ether_sent(self) -> Self:
        """Adds the total sent token amount."""

        totals = sum(amt for _, amt in self._sent)
        self._features[FeaturesEnum.ERC20_TOTAL_ETHER_SENT] = totals
        return self

    def erc20_total_ether_received(self) -> Self:
        """Adds the total received token amount."""

        totals = sum(amt for _, amt in self._received)
        self._features[FeaturesEnum.ERC20_TOTAL_ETHER_RECEIVED] = totals
        return self

    def erc20_uniq_sent_addr(self) -> Self:
        """Adds the number of unique recipient addresses."""

        unique = len({tx.to_address for tx, _ in self._sent})
        self._features[FeaturesEnum.ERC20_UNIQ_SENT_ADDR] = unique
        return self

    def erc20_uniq_rec_addr(self) -> Self:
        """Adds the number of unique sender addresses."""

        unique = len({tx.from_address for tx, _ in self._received})
        self._features[FeaturesEnum.ERC20_UNIQ_REC_ADDR] = unique
        return self

    def erc20_uniq_rec_contract_addr(self) -> Self:
        """Adds the number of unique received token contracts."""

        unique = len({tx.contract_address for tx, _ in self._received})
        self._features[FeaturesEnum.ERC20_UNIQ_REC_CONTRACT_ADDR] = unique
        return self

    def erc20_min_val_sent(self) -> Self:
        """Adds the minimum sent token amount."""

        smallest_sent = min(amt for _, amt in self._sent)
        self._features[FeaturesEnum.ERC20_MIN_VAL_SENT] = smallest_sent
        return self

    def erc20_max_val_sent(self) -> Self:
        """Adds the maximum sent token amount."""

        largest_sent = max(amt for _, amt in self._sent)
        self._features[FeaturesEnum.ERC20_MAX_VAL_SENT] = largest_sent
        return self

    def erc20_avg_val_sent(self) -> Self:
        """Adds the average sent token amount."""

        amounts = [amt for _, amt in self._sent]
        average_sent = sum(amounts) / len(amounts)
        self._features[FeaturesEnum.ERC20_AVG_VAL_SENT] = average_sent
        return self

    def erc20_min_val_rec(self) -> Self:
        """Adds the minimum received token amount."""

        smallest_received = min(amt for _, amt in self._received)
        self._features[FeaturesEnum.ERC20_MIN_VAL_REC] = smallest_received
        return self

    def erc20_max_val_rec(self) -> Self:
        """Adds the maximum received token amount."""

        largest_received = max(amt for _, amt in self._received)
        self._features[FeaturesEnum.ERC20_MAX_VAL_REC] = largest_received
        return self

    def erc20_avg_val_rec(self) -> Self:
        """Adds the average received token amount."""

        amounts = [amt for _, amt in self._received]
        average_received = sum(amounts) / len(amounts)
        self._features[FeaturesEnum.ERC20_AVG_VAL_REC] = average_received
        return self

    def erc20_uniq_sent_token_name(self) -> Self:
        """Adds the number of unique sent token names."""

        unique = len({tx.token_name for tx, _ in self._sent})
        self._features[FeaturesEnum.ERC20_UNIQ_SENT_TOKEN_NAME] = unique
        return self

    def erc20_uniq_rec_token_name(self) -> Self:
        """Adds the number of unique received token names."""

        unique = len({tx.token_name for tx, _ in self._received})
        self._features[FeaturesEnum.ERC20_UNIQ_REC_TOKEN_NAME] = unique
        return self

    def build(self) -> dict[FeaturesEnum, int | Decimal | float]:
        """Returns collected token transfer features."""

        return self._features
