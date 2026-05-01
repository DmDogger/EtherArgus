import pytest

from infrastructure.etherscan_fetcher.dto.raw_etherscan_response_dto import (
    RawEtherscanResponseDTO,
)
from infrastructure.etherscan_fetcher.fetcher.concrete_etherscan_fetcher import (
    ConcreteEtherscanFetcher,
)
from infrastructure.etherscan_fetcher.mapper.etherscan_mapper import EtherscanMapper


class TestConcreteEtherscanFetcher:
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Long http request")
    async def test_get_transactions_returns_dict(
        self, ethereum_address: str, fetcher: ConcreteEtherscanFetcher
    ) -> None:
        res = await fetcher.get_transactions(
            address=ethereum_address,
        )

        assert isinstance(res, dict)

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Long http request")
    async def test_get_internal_transactions_returns_dict(
        self, ethereum_address: str, fetcher: ConcreteEtherscanFetcher
    ) -> None:
        res = await fetcher.get_internal_transactions(address=ethereum_address)

        assert isinstance(res, dict)

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Long http request")
    async def test_get_token_transfers_returns_dict(
        self, ethereum_address: str, fetcher: ConcreteEtherscanFetcher
    ) -> None:
        res = await fetcher.get_token_transfers(address=ethereum_address)

        assert isinstance(res, dict)

    @pytest.mark.asyncio
    async def test_fetch_all_by_taskgroup_returns_dto(
        self, ethereum_address: str, fetcher: ConcreteEtherscanFetcher
    ) -> None:
        result = await fetcher(address=ethereum_address)

        assert isinstance(result, RawEtherscanResponseDTO)
