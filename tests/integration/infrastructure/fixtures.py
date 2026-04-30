from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from aiohttp import ClientSession, TCPConnector


@pytest_asyncio.fixture
async def client() -> AsyncIterator[ClientSession]:
    connector = TCPConnector(ssl=False)
    async with ClientSession(connector=connector) as session:
        yield session


@pytest_asyncio.fixture
async def fetcher(client: ClientSession):
    from infrastructure.etherscan_fetcher.concrete_etherscan_fetcher import (
        ConcreteEtherscanFetcher,
    )

    return ConcreteEtherscanFetcher(client)


@pytest.fixture
def ethereum_address() -> str:
    return f"0xdadB0d80178819F2319190D340ce9A924f783711"
