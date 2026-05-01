import pytest

from infrastructure.etherscan_fetcher.dto.raw_etherscan_response_dto import (
    RawEtherscanResponseDTO,
)
from infrastructure.etherscan_fetcher.fetcher.concrete_etherscan_fetcher import (
    ConcreteEtherscanFetcher,
)
from infrastructure.exceptions import InvalidEtherscanResponseStatus


class TestConcreteEtherscanFetcherUnit:
    @pytest.mark.asyncio
    async def test_fetch_returns_dto(
        self, concrete_etherscan_fetcher: ConcreteEtherscanFetcher
    ) -> None:

        result = await concrete_etherscan_fetcher(address="dummy_address")

        assert isinstance(result, RawEtherscanResponseDTO)

    @pytest.mark.asyncio
    async def test_raises_an_invalid_response_etherscan_instead_of_base_exception(
        self,
        concrete_etherscan_fetcher: ConcreteEtherscanFetcher,
        configure_mock_http_json,
    ) -> None:
        configure_mock_http_json(
            {"status": "0", "message": "NOTOK", "result": "No transactions"}
        )
        with pytest.raises(InvalidEtherscanResponseStatus):
            await concrete_etherscan_fetcher.get_transactions(address="invalid_address")
