from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from aiohttp import ClientSession

from infrastructure.etherscan_fetcher.fetcher.concrete_etherscan_fetcher import (
    ConcreteEtherscanFetcher,
)
from infrastructure.http.clients import AioHTTPClient, EtherscanHTTPClient


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
def concrete_etherscan_fetcher(
    mock_client_session: AsyncMock,
) -> ConcreteEtherscanFetcher:
    return ConcreteEtherscanFetcher(
        EtherscanHTTPClient(AioHTTPClient(mock_client_session)),
    )


@pytest.fixture(scope="class")
def concrete_etherscan_fetcher_class(
    mock_client_session_class: AsyncMock,
) -> ConcreteEtherscanFetcher:
    return ConcreteEtherscanFetcher(
        EtherscanHTTPClient(AioHTTPClient(mock_client_session_class)),
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
    def _set(body: Mapping[str, Any]) -> None:
        mock_http_response.json = AsyncMock(return_value=dict(body))

    return _set
