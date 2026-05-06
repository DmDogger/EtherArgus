import asyncio
from asyncio import TaskGroup
from functools import partial
from typing import final

import structlog

from application.dto.raw_etherscan_response_dto import (
    RawEtherscanPayload,
    RawEtherscanResponseDTO,
)
from application.exceptions.exceptions import InvalidEtherscanResponseStatus
from application.interfaces.done_callback import DoneCallback
from application.interfaces.http_client import EtherscanClient
from config.etherscan import etherscan_settings
from infrastructure.etherscan_fetcher.enums import ActionEnum, ModuleEnum
from infrastructure.etherscan_fetcher.fetcher.etherscan_query_builder import (
    EtherscanQueryBuilder,
    QueryDict,
)

log = structlog.getLogger(__name__)


@final
class ConcreteEtherscanFetcher:
    def __init__(self, client: EtherscanClient, on_done_callback: DoneCallback):
        self._client = client
        self._on_done_callback = on_done_callback
        self._semaphore = asyncio.Semaphore(etherscan_settings.etherscan_api_call_limit)

    async def __call__(self, address: str) -> RawEtherscanResponseDTO:
        """Fetch three Etherscan endpoints concurrently via 'TaskGroup' and a semaphore.

        The free-tier API only allows a handful of requests per minute (e.g. three), so the
        semaphore caps how many calls run at once.

        Each task registers a done-callback that only logs structured metadata; 'partial'
        binds the 'address' because asyncio passes only the 'Task' into that callback.

        After all tasks finish, returns their parsed JSON payloads.
        """
        try:
            async with self._semaphore, TaskGroup() as tg:
                tasks = [
                    tg.create_task(task, name=f"Task:{task.__name__}, Index: {index}")
                    for index, task in enumerate(
                        [
                            self.get_transactions(address=address),
                            self.get_internal_transactions(address=address),
                            self.get_token_transfers(address=address),
                        ]
                    )
                ]

                for task in tasks:
                    task.add_done_callback(
                        partial(self._on_done_callback, address=address)
                    )

            raw_dto = RawEtherscanResponseDTO(
                normal_transactions=tasks[0].result(),
                internal_transactions=tasks[1].result(),
                token_transfers=tasks[2].result(),
            )
            return raw_dto

        except* InvalidEtherscanResponseStatus as err_gr:
            log.error("Etherscan status error", errors=err_gr.exceptions)
            raise
        except* asyncio.TimeoutError as err_gr:
            log.error("HTTP Timeout error", errors=err_gr.exceptions)
            raise

    async def get_transactions(self, *, address: str) -> RawEtherscanPayload:
        """Building and query by 'EtherscanQueryBuilder' and fetching normal transactions by etherscan.io API"""
        query: QueryDict = (
            EtherscanQueryBuilder()
            .address(address=address)
            .action(action=ActionEnum.NORMAL)
            .module(module=ModuleEnum.ACCOUNT)
            .page()
            .sort()
            .build()
        )

        raw_data = await self._client(params=query)
        return raw_data

    async def get_internal_transactions(self, *, address: str) -> RawEtherscanPayload:
        """Building and query by 'EtherscanQueryBuilder' and fetching internal transactions by etherscan.io API"""
        query: QueryDict = (
            EtherscanQueryBuilder()
            .address(address=address)
            .action(action=ActionEnum.INTERNAL)
            .module(module=ModuleEnum.ACCOUNT)
            .page()
            .sort()
            .build()
        )

        raw_data = await self._client(params=query)
        return raw_data

    async def get_token_transfers(self, *, address: str) -> RawEtherscanPayload:
        """Building and query by 'EtherscanQueryBuilder' and fetching token transfers by etherscan.io API"""
        query: QueryDict = (
            EtherscanQueryBuilder()
            .address(address=address)
            .action(action=ActionEnum.TOKEN)
            .module(module=ModuleEnum.ACCOUNT)
            .page()
            .sort()
            .build()
        )

        raw_data = await self._client(params=query)
        return raw_data
