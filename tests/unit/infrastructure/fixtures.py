from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from aiohttp import ClientSession

from infrastructure.etherscan_fetcher.fetcher.concrete_etherscan_fetcher import (
    ConcreteEtherscanFetcher,
)
from infrastructure.etherscan_fetcher.fetcher.etherscan_done_callback import (
    EtherscanDoneCallback,
)
from infrastructure.feature_extractor.enums import FeaturesEnum
from infrastructure.feature_extractor.normal_transactions_feature_builder import (
    NormalTransactionsFeatureBuilder,
)
from infrastructure.http.clients import AioHTTPClient, EtherscanHTTPClient
from infrastructure.etherscan_fetcher.schemas.etherscan_schemas import (
    NormalTransactionSchema,
)


@pytest.fixture
def etherscan_json_ok() -> dict[str, Any]:
    return {"status": "1", "message": "OK", "result": []}


@pytest.fixture
def mock_http_response(etherscan_json_ok: dict[str, Any]) -> AsyncMock:
    response = AsyncMock()
    response.raise_for_status = MagicMock()
    response.json = AsyncMock(return_value=etherscan_json_ok)
    return response


@pytest.fixture
def mock_client_session(mock_http_response: AsyncMock) -> AsyncMock:
    session: AsyncMock = AsyncMock(spec=ClientSession)
    session.get = AsyncMock(return_value=mock_http_response)
    return session


@pytest.fixture
def done_callback() -> EtherscanDoneCallback:
    return EtherscanDoneCallback()


@pytest.fixture
def concrete_etherscan_fetcher(
    mock_client_session: AsyncMock,
    done_callback: EtherscanDoneCallback,
) -> ConcreteEtherscanFetcher:
    return ConcreteEtherscanFetcher(
        EtherscanHTTPClient(AioHTTPClient(mock_client_session)),
        done_callback,
    )


@pytest.fixture(scope="class")
def concrete_etherscan_fetcher_class(
    mock_client_session_class: AsyncMock,
) -> ConcreteEtherscanFetcher:
    return ConcreteEtherscanFetcher(
        EtherscanHTTPClient(AioHTTPClient(mock_client_session_class)),
        EtherscanDoneCallback(),
    )


@pytest.fixture(scope="class")
def mock_http_response_class() -> AsyncMock:
    response = AsyncMock()
    response.raise_for_status = MagicMock()
    response.json = AsyncMock(
        return_value={"status": "1", "message": "OK", "result": []},
    )
    return response


@pytest.fixture(scope="class")
def mock_client_session_class(mock_http_response_class: AsyncMock) -> AsyncMock:
    session: AsyncMock = AsyncMock(spec=ClientSession)
    session.get = AsyncMock(return_value=mock_http_response_class)
    return session


@pytest.fixture
def configure_mock_http_json(mock_http_response: AsyncMock):
    def apply_json_body(body: Mapping[str, Any]) -> None:
        mock_http_response.json = AsyncMock(return_value=dict(body))

    return apply_json_body


@pytest.fixture
def sequence_of_normal_transactions(
    ethereum_address: str,
) -> list[NormalTransactionSchema]:
    counterparty_a = "0x8ba1f109551bd432803012645ac136ddd64dba72"
    counterparty_b = "0xdac17f958d2ee523a2206206994597c13d831ec7"

    raw_transactions: list[dict[str, str]] = [
        {
            "from": ethereum_address,
            "to": counterparty_a,
            "value": "847826712317992291",
            "isError": "0",
            "timeStamp": "1695123400",
        },
        {
            "from": ethereum_address,
            "to": counterparty_b,
            "value": "120000000000000000",
            "isError": "0",
            "timeStamp": "1695124100",
        },
        {
            "from": counterparty_a,
            "to": ethereum_address,
            "value": "500000000000000000",
            "isError": "0",
            "timeStamp": "1695125000",
        },
        {
            "from": counterparty_b,
            "to": ethereum_address,
            "value": "5000000000000000",
            "isError": "0",
            "timeStamp": "1695127200",
        },
        {
            "from": ethereum_address,
            "to": counterparty_a,
            "value": "1",
            "isError": "1",
            "timeStamp": "1695129800",
        },
    ]
    return [
        NormalTransactionSchema.model_validate(row) for row in raw_transactions
    ]


@pytest.fixture
def build_normal_features(
    ethereum_address: str,
    sequence_of_normal_transactions: list[NormalTransactionSchema],
) -> Mapping[FeaturesEnum, int | float | Decimal]:
    return (
        NormalTransactionsFeatureBuilder(
            address=ethereum_address,
            transactions=sequence_of_normal_transactions,
        )
        .total_ether_send()
        .max_value_send()
        .min_value_send()
        .avg_sent()
        .max_value_recv()
        .min_value_recv()
        .avg_recv()
        .unique_sent()
        .unique_recv()
        .time_diff()
        .avg_min_between_sent_tnx()
        .avg_min_between_received_tnx()
        .sent_tnx()
        .unique_received_from_addresses()
        .unique_sent_to_addresses()
        .received_tnx()
        .build()
    )


