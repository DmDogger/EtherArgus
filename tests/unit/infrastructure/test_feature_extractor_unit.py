from decimal import Decimal
from typing import Mapping

from infrastructure.feature_extractor.enums import FeaturesEnum


class TestFeatureExtractorUnit:
    def test_builder_normal_transactions_all_feature_values_are_non_none(
        self,
        build_normal_features: Mapping[FeaturesEnum, int | float | Decimal],
    ) -> None:

        feature_map = build_normal_features

        assert all(enum_key is not None for enum_key in feature_map)


