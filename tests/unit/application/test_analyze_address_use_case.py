from unittest.mock import AsyncMock

import pytest

from application.interfaces.feature_extraction import BuiltFeatures
from application.use_cases.commands.analyze_address_use_case import (
    AnalyzeAddressUseCase,
)


class TestAnalyzeAddressUseCaseUnit:
    @pytest.mark.asyncio
    async def test_build_features_use_case_receives_address(
        self,
        sample_eth_address: str,
        analyze_address_use_case: AnalyzeAddressUseCase,
        mock_build_features_use_case: AsyncMock,
    ) -> None:
        await analyze_address_use_case(address=sample_eth_address)

        mock_build_features_use_case.assert_awaited_once_with(
            address=sample_eth_address
        )

    @pytest.mark.asyncio
    async def test_classify_use_case_receives_built_features_stub(
        self,
        sample_eth_address: str,
        analyze_address_use_case: AnalyzeAddressUseCase,
        mock_classify_fraud_use_case: AsyncMock,
        built_features_stub: BuiltFeatures,
    ) -> None:
        await analyze_address_use_case(address=sample_eth_address)

        mock_classify_fraud_use_case.assert_awaited_once_with(built_features_stub)

    @pytest.mark.asyncio
    async def test_save_analysis_results_use_case_awaited_once(
        self,
        sample_eth_address: str,
        analyze_address_use_case: AnalyzeAddressUseCase,
        mock_save_analysis_results_use_case: AsyncMock,
    ) -> None:
        await analyze_address_use_case(address=sample_eth_address)

        mock_save_analysis_results_use_case.assert_awaited_once()
