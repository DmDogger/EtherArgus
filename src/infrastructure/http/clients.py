import asyncio
from typing import Mapping, final

import stamina
from aiohttp import ClientSession

from application.dto.raw_etherscan_response_dto import RawEtherscanPayload
from application.interfaces.http_client import HTTPClient
from config.etherscan import etherscan_settings
from infrastructure.etherscan.building.etherscan_query_builder import QueryDict
from infrastructure.exceptions import InvalidEtherscanResponseStatus

type HTTPResponse = Mapping[str, str | list[dict[str, str]]]


class AioHTTPClient:
    def __init__(self, client: ClientSession):
        self._client = client

    @stamina.retry(on=asyncio.TimeoutError, attempts=3)
    async def get[K, V](
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
    ) -> RawEtherscanPayload:
        response = await self._client.get(
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
