import asyncio
from typing import Mapping, final

import stamina
from aiohttp import ClientSession

from application.interfaces.http_client import HTTPClient
from config.etherscan import etherscan_settings
from infrastructure.etherscan_fetcher.fetcher.concrete_etherscan_fetcher import (
    RawQueryFromEtherscan,
)
from infrastructure.etherscan_fetcher.fetcher.etherscan_query_builder import QueryDict
from infrastructure.exceptions import InvalidEtherscanResponseStatus

type HTTPResponse = Mapping[str, str | list[dict[str, str]]]


class AioHTTPClient:
    def __init__(self, client: ClientSession):
        self._client = client

    @stamina.retry(on=asyncio.TimeoutError, attempts=3)
    async def __call__[K, V](
        self, params: dict[K, V], url: str | None = None
    ) -> HTTPResponse:
        response = await self._client.get(url=url, params=params)

        response.raise_for_status()
        raw_data = await response.json()

        return raw_data

@final
class EtherscanHTTPClient:
    def __init__(self, client: HTTPClient):
        self._client = client

    async def __call__(
        self, params: QueryDict, url: str | None = None
    ) -> RawQueryFromEtherscan:
        response = await self._client(
            url=url if url is not None else etherscan_settings.etherscan_url,
            params=params,
        )

        response_status = response["status"]
        response_message = response["message"]

        if response_status != "1":
            raise InvalidEtherscanResponseStatus(
                f"Expected status to be '1' but got: {response_status}\n"
                f"Reason: {response_message}"
            )

        return response
