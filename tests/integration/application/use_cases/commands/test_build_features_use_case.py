from decimal import Decimal

import pytest

from application.interfaces.use_cases.build_features import BuildFeaturesUseCase


class TestBuildFeaturesUseCase:
    @pytest.mark.asyncio
    async def test_use_case_building_features_correctly(
        self, ethereum_address: str, build_features_use_case: BuildFeaturesUseCase
    ) -> None:
        build_features = await build_features_use_case(address=ethereum_address)

        assert all(
            isinstance(features, (int, float, Decimal))
            for features in build_features.values()
        )
