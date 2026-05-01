from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from aiohttp import ClientSession, TCPConnector


@pytest_asyncio.fixture
async def aiohttp_client_session() -> AsyncIterator[ClientSession]:
    connector = TCPConnector(ssl=False)
    async with ClientSession(connector=connector) as session:
        yield session


@pytest_asyncio.fixture
async def etherscan_fetcher(
    aiohttp_client_session: ClientSession,
):
    from infrastructure.etherscan_fetcher.fetcher.concrete_etherscan_fetcher import (
        ConcreteEtherscanFetcher,
    )
    from infrastructure.etherscan_fetcher.fetcher.etherscan_done_callback import (
        EtherscanDoneCallback,
    )
    from infrastructure.http.clients import AioHTTPClient, EtherscanHTTPClient

    return ConcreteEtherscanFetcher(
        EtherscanHTTPClient(AioHTTPClient(aiohttp_client_session)),
        EtherscanDoneCallback(),
    )


@pytest.fixture
def ethereum_address() -> str:
    return "0xdadB0d80178819F2319190D340ce9A924f783711"
