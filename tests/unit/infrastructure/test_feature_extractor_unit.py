from decimal import Decimal
from typing import Mapping

import pytest

from infrastructure.feature_extractor.enums import FeaturesEnum

type FeatureValue = int | float | Decimal


class TestFeatureExtractorUnit:
    def test_builder_normal_transactions_all_feature_values_are_non_none(
        self,
        build_normal_features: Mapping[FeaturesEnum, int | float | Decimal],
    ) -> None:

        feature_map = build_normal_features

        assert all(enum_key is not None for enum_key in feature_map)

    @pytest.mark.parametrize(
        ("feature", "expected_value"),
        [
            (FeaturesEnum.NUMBER_OF_CREATED_CONTRACTS, 2),
            (
                FeaturesEnum.TOTAL_ETHER_SENT_CONTRACTS,
                Decimal("3700000000000000000"),
            ),
        ],
    )
    def test_builder_internal_transactions_feature_value(
        self,
        build_internal_features: Mapping[FeaturesEnum, FeatureValue],
        feature: FeaturesEnum,
        expected_value: FeatureValue,
    ) -> None:
        assert build_internal_features[feature] == expected_value

    @pytest.mark.parametrize(
        ("feature", "expected_value"),
        [
            (FeaturesEnum.TOTAL_ERC20_TNX, 4),
            (FeaturesEnum.ERC20_TOTAL_ETHER_SENT, Decimal(3)),
            (FeaturesEnum.ERC20_TOTAL_ETHER_RECEIVED, Decimal(4)),
            (FeaturesEnum.ERC20_UNIQ_SENT_ADDR, 2),
            (FeaturesEnum.ERC20_UNIQ_REC_ADDR, 2),
            (FeaturesEnum.ERC20_UNIQ_REC_CONTRACT_ADDR, 2),
            (FeaturesEnum.ERC20_MIN_VAL_SENT, Decimal(1)),
            (FeaturesEnum.ERC20_MAX_VAL_SENT, Decimal(2)),
            (FeaturesEnum.ERC20_AVG_VAL_SENT, Decimal("1.5")),
            (FeaturesEnum.ERC20_MIN_VAL_REC, Decimal(1)),
            (FeaturesEnum.ERC20_MAX_VAL_REC, Decimal(3)),
            (FeaturesEnum.ERC20_AVG_VAL_REC, Decimal(2)),
            (FeaturesEnum.ERC20_UNIQ_SENT_TOKEN_NAME, 2),
            (FeaturesEnum.ERC20_UNIQ_REC_TOKEN_NAME, 2),
        ],
    )
    def test_builder_token_transfers_feature_value(
        self,
        build_token_transfer_features: Mapping[FeaturesEnum, FeatureValue],
        feature: FeaturesEnum,
        expected_value: FeatureValue,
    ) -> None:
        assert build_token_transfer_features[feature] == expected_value
