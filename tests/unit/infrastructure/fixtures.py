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
from infrastructure.feature_extractor.internal_transactions_feature_builder import (
    InternalTransactionsFeatureBuilder,
)
from infrastructure.feature_extractor.normal_transactions_feature_builder import (
    NormalTransactionsFeatureBuilder,
)
from infrastructure.feature_extractor.token_transfers_feature_builder import (
    TokenTransfersFeatureBuilder,
)
from infrastructure.http.clients import AioHTTPClient, EtherscanHTTPClient
from infrastructure.etherscan_fetcher.schemas.etherscan_schemas import (
    InternalTransactionSchema,
    NormalTransactionSchema,
    TokenTransfersSchema,
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
    return [NormalTransactionSchema.model_validate(row) for row in raw_transactions]


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


@pytest.fixture
def sequence_of_internal_transactions(
    ethereum_address: str,
) -> tuple[InternalTransactionSchema, ...]:
    counterparty = "0x1000000000000000000000000000000000000001"
    raw_transactions = (
        {
            "from": ethereum_address,
            "to": counterparty,
            "value": "1000000000000000000",
            "isError": "0",
            "timeStamp": "1695123400",
            "type": "create",
        },
        {
            "from": ethereum_address,
            "to": counterparty,
            "value": "2000000000000000000",
            "isError": "0",
            "timeStamp": "1695124000",
            "type": "create",
        },
        {
            "from": counterparty,
            "to": ethereum_address,
            "value": "700000000000000000",
            "isError": "0",
            "timeStamp": "1695125000",
            "type": "call",
        },
    )
    return tuple(
        InternalTransactionSchema.model_validate(row) for row in raw_transactions
    )


@pytest.fixture
def build_internal_features(
    ethereum_address: str,
    sequence_of_internal_transactions: tuple[InternalTransactionSchema, ...],
) -> Mapping[FeaturesEnum, int | float | Decimal]:
    return (
        InternalTransactionsFeatureBuilder(
            address=ethereum_address,
            transactions=sequence_of_internal_transactions,
        )
        .number_of_created_contracts()
        .total_ether_sent_contracts()
        .build()
    )


@pytest.fixture
def sequence_of_token_transfers(
    ethereum_address: str,
) -> tuple[TokenTransfersSchema, ...]:
    counterparty_a = "0x2000000000000000000000000000000000000002"
    counterparty_b = "0x3000000000000000000000000000000000000003"
    contract_a = "0x4000000000000000000000000000000000000004"
    contract_b = "0x5000000000000000000000000000000000000005"
    raw_transfers = (
        {
            "from": ethereum_address,
            "to": counterparty_a,
            "value": "1000000000000000000",
            "tokenDecimal": "18",
            "contractAddress": contract_a,
            "tokenName": "Alpha",
            "isError": "0",
            "timeStamp": "1695123400",
        },
        {
            "from": ethereum_address,
            "to": counterparty_b,
            "value": "2000000000000000000",
            "tokenDecimal": "18",
            "contractAddress": contract_b,
            "tokenName": "Beta",
            "isError": "0",
            "timeStamp": "1695124000",
        },
        {
            "from": counterparty_a,
            "to": ethereum_address,
            "value": "1000000",
            "tokenDecimal": "6",
            "contractAddress": contract_a,
            "tokenName": "Alpha",
            "isError": "0",
            "timeStamp": "1695125000",
        },
        {
            "from": counterparty_b,
            "to": ethereum_address,
            "value": "3000000",
            "tokenDecimal": "6",
            "contractAddress": contract_b,
            "tokenName": "Gamma",
            "isError": "0",
            "timeStamp": "1695126000",
        },
    )
    return tuple(TokenTransfersSchema.model_validate(row) for row in raw_transfers)


@pytest.fixture
def build_token_transfer_features(
    ethereum_address: str,
    sequence_of_token_transfers: tuple[TokenTransfersSchema, ...],
) -> Mapping[FeaturesEnum, int | float | Decimal]:
    return (
        TokenTransfersFeatureBuilder(
            address=ethereum_address,
            transfers=sequence_of_token_transfers,
        )
        .total_erc20_tnx()
        .erc20_total_ether_sent()
        .erc20_total_ether_received()
        .erc20_uniq_sent_addr()
        .erc20_uniq_rec_addr()
        .erc20_uniq_rec_contract_addr()
        .erc20_min_val_sent()
        .erc20_max_val_sent()
        .erc20_avg_val_sent()
        .erc20_min_val_rec()
        .erc20_max_val_rec()
        .erc20_avg_val_rec()
        .erc20_uniq_sent_token_name()
        .erc20_uniq_rec_token_name()
        .build()
    )
