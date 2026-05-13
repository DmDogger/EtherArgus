import pytest

from application.dto.raw_etherscan_response_dto import RawEtherscanResponseDTO
from infrastructure.etherscan.fetching.concrete_etherscan_fetcher import (
    ConcreteEtherscanFetcher,
)
from infrastructure.exceptions import InvalidEtherscanResponseStatus


class TestConcreteEtherscanFetcherUnit:
    @pytest.mark.asyncio
    async def test_fetch_returns_dto(
        self, concrete_etherscan_fetcher: ConcreteEtherscanFetcher
    ) -> None:

        response_dto = await concrete_etherscan_fetcher(address="dummy_address")

        assert isinstance(response_dto, RawEtherscanResponseDTO)
