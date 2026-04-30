import pytest

from infrastructure.etherscan_fetcher.fetcher.concrete_etherscan_fetcher import (
    ConcreteEtherscanFetcher,
)


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
    @pytest.mark.skip(reason="Long http request")
    async def test_fetch_all_by_taskgroup_returns_correct_counter_results(
        self, ethereum_address: str, fetcher: ConcreteEtherscanFetcher
    ) -> None:
        result = await fetcher(address=ethereum_address)

        assert len(result) == 3
