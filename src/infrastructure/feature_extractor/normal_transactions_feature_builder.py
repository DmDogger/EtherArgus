from collections.abc import Sequence
from decimal import Decimal
from typing import Self

from infrastructure.etherscan_fetcher.schemas.etherscan_schemas import (
    NormalTransactionSchema,
)
from infrastructure.feature_extractor.enums import FeaturesEnum


class NormalTransactionsFeatureBuilder:
    _features: dict[FeaturesEnum, int | Decimal | float]

    def __init__(self, address: str, transactions: Sequence[NormalTransactionSchema]):
        self._transactions = set(filter(lambda tx: tx.is_error == 0, transactions))
        self._address = address
        self._received = set(
            tx for tx in self._transactions if self._address == tx.to_address
        )
        self._sent = set(
            tx for tx in self._transactions if self._address == tx.from_address
        )
        self._features = {}

    def total_ether_send(self) -> Self:
        sent_total = sum([Decimal(tx.value) for tx in self._sent])
        self._features[FeaturesEnum.TOTAL_ETHEREUM_SENT] = sent_total
        return self

    def min_value_send(self) -> Self:
        smallest_sent = min([Decimal(tx.value) for tx in self._sent])
        self._features[FeaturesEnum.MIN_VALUE_SENT] = smallest_sent
        return self

    def max_value_send(self) -> Self:
        largest_sent = max([Decimal(tx.value) for tx in self._sent])
        self._features[FeaturesEnum.MAX_VALUE_SENT] = largest_sent
        return self

    def total_ether_recv(self) -> Self:
        received_total = sum([Decimal(tx.value) for tx in self._received])
        self._features[FeaturesEnum.TOTAL_ETHEREUM_REC] = received_total
        return self

    def min_value_recv(self) -> Self:
        smallest_received = min([Decimal(tx.value) for tx in self._received])
        self._features[FeaturesEnum.MIN_VALUE_REC] = smallest_received
        return self

    def max_value_recv(self) -> Self:
        largest_received = max([Decimal(tx.value) for tx in self._received])
        self._features[FeaturesEnum.MAX_VALUE_REC] = largest_received
        return self

    def avg_sent(self) -> Self:
        sent_sum = sum([Decimal(tx.value) for tx in self._sent])
        sent_count = len([tx.value for tx in self._sent])
        average_sent_value = sent_sum / sent_count
        self._features[FeaturesEnum.AVG_SENT] = average_sent_value
        return self

    def avg_recv(self) -> Self:
        recv_sum = sum([Decimal(tx.value) for tx in self._received])
        recv_count = len([tx.value for tx in self._received])
        average_recv_value = recv_sum / recv_count
        self._features[FeaturesEnum.AVG_REC] = average_recv_value
        return self

    def unique_sent(self) -> Self:
        distinct_recipient_addresses = len({tx.to_address for tx in self._sent})
        self._features[FeaturesEnum.UNIQUE_SENT] = distinct_recipient_addresses
        return self

    def unique_recv(self) -> Self:
        distinct_sender_addresses = len({tx.from_address for tx in self._received})
        self._features[FeaturesEnum.UNIQUE_RECV] = distinct_sender_addresses
        return self

    def time_diff(self) -> Self:
        timestamps = [tx.timestamp for tx in self._transactions]
        newest_timestamp, oldest_timestamp = max(timestamps), min(timestamps)
        delta_minutes = (newest_timestamp - oldest_timestamp) / 60
        self._features[FeaturesEnum.TIME_DIFF_FIRST_LAST] = delta_minutes
        return self

    def avg_min_between_sent_tnx(self) -> Self:
        timestamps = sorted([tx.timestamp for tx in self._sent])
        later_timestamps = timestamps[1:]

        deltas_minutes = [
            (earlier_ts - later_ts) / 60
            for earlier_ts, later_ts in zip(timestamps, later_timestamps)
        ]

        average_delta_minutes = sum(deltas_minutes) / len(deltas_minutes)

        self._features[FeaturesEnum.AVG_TIME_BETWEEN_SENT] = average_delta_minutes

        return self

    def sent_tnx(self) -> Self:
        self._features[FeaturesEnum.SENT_TNX] = len(self._sent)
        return self

    def received_tnx(self) -> Self:
        self._features[FeaturesEnum.RECEIVED_TNX] = len(self._received)
        return self

    def unique_sent_to_addresses(self) -> Self:
        self._features[FeaturesEnum.UNIQUE_SENT_TO_ADDRESSES] = len(
            {tx.to_address for tx in self._sent}
        )
        return self

    def unique_received_from_addresses(self) -> Self:
        self._features[FeaturesEnum.UNIQUE_RECEIVED_FROM_ADDRESSES] = len(
            {tx.from_address for tx in self._received}
        )
        return self

    def avg_min_between_received_tnx(self) -> Self:
        timestamps = sorted([tx.timestamp for tx in self._received])
        later_timestamps = timestamps[1:]
        deltas_minutes = [
            (later - earlier) / 60
            for earlier, later in zip(timestamps, later_timestamps)
        ]
        average_delta_minutes = sum(deltas_minutes) / len(deltas_minutes)
        self._features[FeaturesEnum.AVG_TIME_BETWEEN_RECEIVED] = average_delta_minutes
        return self

    def build(self) -> dict[FeaturesEnum, int | Decimal]:
        return self._features
