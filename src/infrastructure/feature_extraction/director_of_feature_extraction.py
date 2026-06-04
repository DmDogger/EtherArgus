from collections.abc import Sequence

from application.dto.etherscan_transaction_dtos import (
    InternalTransactionDTO,
    NormalTransactionDTO,
    TokenTransfersDTO,
)
from application.interfaces.features.feature_extraction import (
    BuiltFeatures,
    InternalTransactionsFeatureBuilder,
    NormalTransactionsFeatureBuilder,
)
from infrastructure.feature_extraction.internal_transactions_feature_builder import (
    InternalTransactionsFeatureBuilder as ConcreteInternalTransactionsFeatureBuilder,
)
from infrastructure.feature_extraction.normal_transactions_feature_builder import (
    NormalTransactionsFeatureBuilder as ConcreteNormalTransactionsFeatureBuilder,
)
from infrastructure.feature_extraction.token_transfers_feature_builder import (
    TokenTransfersFeatureBuilder,
)


class DirectorOfFeatureExtraction:
    """Runs feature-builder chains for each Etherscan transaction group."""

    def build_features(
        self,
        address: str,
        normal_transactions: Sequence[NormalTransactionDTO],
        internal_transactions: Sequence[InternalTransactionDTO],
        token_transfers: Sequence[TokenTransfersDTO],
    ) -> BuiltFeatures:
        """Builds and merges aggregate features from all transaction groups."""

        normal_builder, internal_builder, token_transfers_builder = (
            self._build_builders(
                address=address,
                normal_transactions=normal_transactions,
                internal_transactions=internal_transactions,
                token_transfers=token_transfers,
            )
        )

        from_normal_transactions = self._build_features_from_normal_transactions(
            builder=normal_builder
        )
        from_internal_transactions = self._build_features_from_internal_transactions(
            builder=internal_builder
        )
        from_token_transfers = self._build_features_from_token_transfers(
            builder=token_transfers_builder
        )

        merged = (
            from_normal_transactions | from_internal_transactions | from_token_transfers
        )

        return merged

    def _build_features_from_normal_transactions(
        self, builder: NormalTransactionsFeatureBuilder
    ) -> BuiltFeatures:
        """Builds aggregate features from normal transactions."""

        _features: BuiltFeatures = (
            builder.total_ether_send()
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
            .avg_min_between_received_tnx()
            .build()
        )
        return _features

    def _build_features_from_internal_transactions(
        self, builder: InternalTransactionsFeatureBuilder
    ) -> BuiltFeatures:
        """Builds aggregate features from internal transactions."""

        _features: BuiltFeatures = (
            builder.number_of_created_contracts().total_ether_sent_contracts().build()
        )
        return _features

    def _build_features_from_token_transfers(
        self, builder: TokenTransfersFeatureBuilder
    ) -> BuiltFeatures:
        """Builds aggregate features from ERC-20 token transfers."""

        _features: BuiltFeatures = (
            builder.total_erc20_tnx()
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

    @staticmethod
    def _build_builders(
        address: str,
        normal_transactions: Sequence[NormalTransactionDTO],
        internal_transactions: Sequence[InternalTransactionDTO],
        token_transfers: Sequence[TokenTransfersDTO],
    ):
        _normal_builder = ConcreteNormalTransactionsFeatureBuilder(
            address,
            normal_transactions,
        )
        _internal_builder = ConcreteInternalTransactionsFeatureBuilder(
            address,
            internal_transactions,
        )
        _token_builder = TokenTransfersFeatureBuilder(address, token_transfers)
        return _normal_builder, _internal_builder, _token_builder
