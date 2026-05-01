from collections.abc import Sequence
from decimal import Decimal

from infrastructure.etherscan_fetcher.schemas.etherscan_schemas import (
    InternalTransactionSchema,
    NormalTransactionSchema,
    TokenTransfersSchema,
)
from infrastructure.feature_extractor.enums import FeaturesEnum
from infrastructure.feature_extractor.internal_transactions_feature_builder import (
    InternalTransactionsFeatureBuilder,
)
from infrastructure.feature_extractor.normal_transactions_feature_builder import (
    NormalTransactionsFeatureBuilder,
)
from infrastructure.feature_extractor.token_transfers_feature_builder import (
    TokenTransfersFeatureBuilder,
)

type BuiltFeatures = dict[FeaturesEnum, int | Decimal | float]


class DirectorOfFeatureExtraction:
    """Runs feature-builder chains for each Etherscan transaction group."""

    def __init__(
        self,
        address: str,
        normal_transactions: Sequence[NormalTransactionSchema],
        internal_transactions: Sequence[InternalTransactionSchema],
        token_transfers: Sequence[TokenTransfersSchema],
    ):
        self._normal_builder = NormalTransactionsFeatureBuilder(
            address,
            normal_transactions,
        )
        self._internal_builder = InternalTransactionsFeatureBuilder(
            address,
            internal_transactions,
        )
        self._token_builder = TokenTransfersFeatureBuilder(address, token_transfers)

    def __call__(self) -> BuiltFeatures:
        """Builds and merges aggregate features from all transaction groups."""

        from_normal_transactions = self._build_features_from_normal_transactions()
        from_internal_transactions = self._build_features_from_internal_transactions()
        from_token_transfers = self._build_features_from_token_transfers()

        merged = (
            from_normal_transactions | from_internal_transactions | from_token_transfers
        )

        return merged

    def _build_features_from_normal_transactions(self) -> BuiltFeatures:
        """Builds aggregate features from normal transactions."""

        _features: BuiltFeatures = (
            self._normal_builder.total_ether_send()
            .min_value_send()
            .max_value_send()
            .total_ether_recv()
            .min_value_recv()
            .max_value_recv()
            .avg_sent()
            .avg_recv()
            .unique_sent()
            .unique_recv()
            .time_diff()
            .avg_min_between_sent_tnx()
            .sent_tnx()
            .received_tnx()
            .unique_sent_to_addresses()
            .unique_received_from_addresses()
            .avg_min_between_received_tnx()
            .build()
        )
        return _features

    def _build_features_from_internal_transactions(self) -> BuiltFeatures:
        """Builds aggregate features from internal transactions."""

        _features: BuiltFeatures = (
            self._internal_builder.number_of_created_contracts()
            .total_ether_sent_contracts()
            .build()
        )
        return _features

    def _build_features_from_token_transfers(self) -> BuiltFeatures:
        """Builds aggregate features from ERC-20 token transfers."""

        _features: BuiltFeatures = (
            self._token_builder.total_erc20_tnx()
            .erc20_total_ether_sent()
            .erc20_total_ether_received()
            .erc20_uniq_sent_addr()
            .erc20_uniq_rec_addr()
            .erc20_uniq_rec_contract_addr()
            .erc20_min_val_sent()
            .erc20_max_val_sent()
            .erc20_avg_val_sent()
            .erc20_min_val_rec()
            .erc20_max_val_rec()
            .erc20_avg_val_rec()
            .erc20_uniq_sent_token_name()
            .erc20_uniq_rec_token_name()
            .build()
        )
        return _features
