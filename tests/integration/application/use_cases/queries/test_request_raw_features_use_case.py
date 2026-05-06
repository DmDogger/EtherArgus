import pytest

from application.dto.raw_etherscan_response_dto import RawEtherscanResponseDTO
from application.interfaces.request_raw_features import RequestRawFeaturesUseCase


class TestRequestRawFeaturesUseCase:
    @pytest.mark.asyncio
    async def test_use_case_requests_correctly_and_returns_raw_features_dto(
        self,
        ethereum_address: str,
        request_features_use_case: RequestRawFeaturesUseCase,
    ) -> None:
        response: RawEtherscanResponseDTO = await request_features_use_case(
            address=ethereum_address
        )

        assert isinstance(response, RawEtherscanResponseDTO)
