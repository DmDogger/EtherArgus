from collections.abc import Sequence
from decimal import Decimal
from typing import Self

from infrastructure.etherscan_fetcher.schemas.etherscan_schemas import (
    InternalTransactionSchema,
)
from infrastructure.feature_extractor.enums import FeaturesEnum


class InternalTransactionsFeatureBuilder:
    """Builds aggregate features from internal transactions."""

    _features: dict[FeaturesEnum, int | Decimal | float]

    def __init__(self, address: str, transactions: Sequence[InternalTransactionSchema]):
        self._address = address
        self._transactions = tuple(transactions)
        self._features = {}

    def number_of_created_contracts(self) -> Self:
        """Adds the number of contract creation internal transactions."""

        created = sum(1 for tx in self._transactions if tx.type == "create")
        self._features[FeaturesEnum.NUMBER_OF_CREATED_CONTRACTS] = created
        return self

    def total_ether_sent_contracts(self) -> Self:
        """Adds the total value across internal transactions."""

        totals = sum(Decimal(tx.value) for tx in self._transactions)
        self._features[FeaturesEnum.TOTAL_ETHER_SENT_CONTRACTS] = totals
        return self

    def build(self) -> dict[FeaturesEnum, int | Decimal | float]:
        """Returns collected internal transaction features."""

        return self._features
