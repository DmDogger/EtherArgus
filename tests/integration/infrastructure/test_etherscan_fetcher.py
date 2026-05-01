import pytest

from infrastructure.etherscan_fetcher.dto.raw_etherscan_response_dto import (
    RawEtherscanResponseDTO,
)
from infrastructure.etherscan_fetcher.fetcher.concrete_etherscan_fetcher import (
    ConcreteEtherscanFetcher,
)


class TestConcreteEtherscanFetcher:
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Long http request")
    async def test_get_transactions_returns_dict(
        self, ethereum_address: str, etherscan_fetcher: ConcreteEtherscanFetcher
    ) -> None:
        response_payload = await etherscan_fetcher.get_transactions(
            address=ethereum_address,
        )

        assert isinstance(response_payload, dict)

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Long http request")
    async def test_get_internal_transactions_returns_dict(
        self, ethereum_address: str, etherscan_fetcher: ConcreteEtherscanFetcher
    ) -> None:
        response_payload = await etherscan_fetcher.get_internal_transactions(
            address=ethereum_address,
        )

        assert isinstance(response_payload, dict)

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Long http request")
    async def test_get_token_transfers_returns_dict(
        self, ethereum_address: str, etherscan_fetcher: ConcreteEtherscanFetcher
    ) -> None:
        response_payload = await etherscan_fetcher.get_token_transfers(
            address=ethereum_address,
        )

        assert isinstance(response_payload, dict)

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Long http request")
    async def test_fetch_all_by_taskgroup_returns_dto(
        self, ethereum_address: str, etherscan_fetcher: ConcreteEtherscanFetcher
    ) -> None:
        response_dto = await etherscan_fetcher(address=ethereum_address)

        assert isinstance(response_dto, RawEtherscanResponseDTO)
