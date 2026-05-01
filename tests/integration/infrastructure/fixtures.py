from collections.abc import AsyncIterator, Sequence

import pytest
import pytest_asyncio
from aiohttp import ClientSession, TCPConnector

from infrastructure.etherscan_fetcher.dto.raw_etherscan_response_dto import (
    RawEtherscanResponseDTO,
)
from infrastructure.etherscan_fetcher.mapper.etherscan_mapper import EtherscanMapper
from infrastructure.etherscan_fetcher.schemas.etherscan_schemas import (
    InternalTransactionSchema,
    NormalTransactionSchema,
    TokenTransfersSchema,
)
from infrastructure.feature_extractor.director_of_feature_extraction import (
    DirectorOfFeatureExtraction,
)
from infrastructure.feature_extractor.internal_transactions_feature_builder import (
    InternalTransactionsFeatureBuilder,
)
from infrastructure.feature_extractor.normal_transactions_feature_builder import (
    NormalTransactionsFeatureBuilder,
)
from infrastructure.feature_extractor.token_transfers_feature_builder import (
    TokenTransfersFeatureBuilder,
)


_DEFAULT_ETHEREUM_ADDRESS = (
    "0xdadB0d80178819F2319190D340ce9A924f783711"
)


@pytest.fixture
def ethereum_address(request: pytest.FixtureRequest) -> str:
    param = getattr(request, "param", None)
    if param is None:
        return _DEFAULT_ETHEREUM_ADDRESS
    return str(param)


@pytest.fixture
def etherscan_mapper() -> EtherscanMapper:
    return EtherscanMapper()


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


@pytest_asyncio.fixture
async def make_director_of_feature_extraction(
    etherscan_fetcher,
    etherscan_mapper: EtherscanMapper,
):
    async def _factory(address: str) -> DirectorOfFeatureExtraction:
        dto = await etherscan_fetcher(address)
        normal = etherscan_mapper.from_raw_normal_transactions(dto)
        internal = etherscan_mapper.from_raw_internal_transactions(dto)
        tokens = etherscan_mapper.from_raw_token_transfers(dto)
        return DirectorOfFeatureExtraction(address, normal, internal, tokens)

    return _factory


@pytest_asyncio.fixture
async def raw_etherscan_response_dto(
    ethereum_address: str,
    etherscan_fetcher,
) -> RawEtherscanResponseDTO:
    return await etherscan_fetcher(address=ethereum_address)


@pytest_asyncio.fixture
async def transactions(
    etherscan_mapper: EtherscanMapper,
    raw_etherscan_response_dto: RawEtherscanResponseDTO,
) -> list[NormalTransactionSchema]:
    return etherscan_mapper.from_raw_normal_transactions(raw_etherscan_response_dto)


@pytest_asyncio.fixture
async def internal_transactions(
    etherscan_mapper: EtherscanMapper,
    raw_etherscan_response_dto: RawEtherscanResponseDTO,
) -> list[InternalTransactionSchema]:
    return etherscan_mapper.from_raw_internal_transactions(raw_etherscan_response_dto)


@pytest_asyncio.fixture
async def token_transfers(
    etherscan_mapper: EtherscanMapper,
    raw_etherscan_response_dto: RawEtherscanResponseDTO,
) -> list[TokenTransfersSchema]:
    return etherscan_mapper.from_raw_token_transfers(raw_etherscan_response_dto)


@pytest_asyncio.fixture
async def normal_builder(
    ethereum_address: str,
    transactions: Sequence[NormalTransactionSchema],
) -> NormalTransactionsFeatureBuilder:
    return NormalTransactionsFeatureBuilder(ethereum_address, transactions)


@pytest_asyncio.fixture
async def internal_builder(
    ethereum_address: str,
    internal_transactions: Sequence[InternalTransactionSchema],
) -> InternalTransactionsFeatureBuilder:
    return InternalTransactionsFeatureBuilder(
        ethereum_address,
        internal_transactions,
    )


@pytest_asyncio.fixture
async def token_builder(
    ethereum_address: str,
    token_transfers: Sequence[TokenTransfersSchema],
) -> TokenTransfersFeatureBuilder:
    return TokenTransfersFeatureBuilder(ethereum_address, token_transfers)


@pytest_asyncio.fixture
async def director_of_feature_builder(
    ethereum_address: str,
    transactions: Sequence[NormalTransactionSchema],
    internal_transactions: Sequence[InternalTransactionSchema],
    token_transfers: Sequence[TokenTransfersSchema],
) -> DirectorOfFeatureExtraction:
    return DirectorOfFeatureExtraction(
        ethereum_address,
        transactions,
        internal_transactions,
        token_transfers,
    )
