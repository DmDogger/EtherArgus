import asyncio
from asyncio import TaskGroup, Task
from datetime import UTC, datetime
from functools import partial
from typing import Mapping, Sequence

import structlog

from application.interfaces.http_client import HTTPClient
from config.etherscan import etherscan_settings
from infrastructure.etherscan_fetcher.enums import ActionEnum, TaskStatusEnum
from infrastructure.etherscan_fetcher.fetcher.etherscan_query_builder import (
    EtherscanQueryBuilder,
    QueryDict,
)
from infrastructure.exceptions import InvalidEtherscanResponseStatus

type RawQueryFromEtherscan = Mapping[str, str | list[dict[str, str]]]

log = structlog.getLogger(__name__)


class ConcreteEtherscanFetcher:
    def __init__(self, client: HTTPClient):
        self._client = client
        self._semaphore = asyncio.Semaphore(etherscan_settings.etherscan_api_call_limit)

    async def __call__(self, address: str) -> Sequence[RawQueryFromEtherscan]:
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
                    task.add_done_callback(partial(self._done_cb, address=address))

            return [t.result() for t in tasks]
        except* InvalidEtherscanResponseStatus as err_gr:
            log.error("Etherscan status error", errors=err_gr.exceptions)
            raise
        except* asyncio.TimeoutError as err_gr:
            log.error("HTTP Timeout error", errors=err_gr.exceptions)
            raise

    async def get_transactions(self, *, address: str) -> RawQueryFromEtherscan:
        """Building and query by 'EtherscanQueryBuilder' and fetching normal transactions by etherscan.io API"""
        query: QueryDict = (
            EtherscanQueryBuilder()
            .address(address=address)
            .action(action=ActionEnum.NORMAL)
            .module(module="account")
            .page()
            .sort()
            .build()
        )

        raw_data = await self._client(params=query)
        return raw_data

    async def get_internal_transactions(self, *, address: str) -> RawQueryFromEtherscan:
        """Building and query by 'EtherscanQueryBuilder' and fetching internal transactions by etherscan.io API"""
        query: QueryDict = (
            EtherscanQueryBuilder()
            .address(address=address)
            .action(action=ActionEnum.INTERNAL)
            .module(module="account")
            .page()
            .sort()
            .build()
        )

        raw_data = await self._client(params=query)
        return raw_data

    async def get_token_transfers(self, *, address: str) -> RawQueryFromEtherscan:
        """Building and query by 'EtherscanQueryBuilder' and fetching token transfers by etherscan.io API"""
        query: QueryDict = (
            EtherscanQueryBuilder()
            .address(address=address)
            .action(action=ActionEnum.TOKEN)
            .module(module="account")
            .page()
            .sort()
            .build()
        )

        raw_data = await self._client(params=query)
        return raw_data

    @staticmethod
    def _done_cb(task: Task, address: str) -> None:
        task_name = task.get_name()
        coro_name = task.get_coro().__name__
        if task.cancelled():
            log.info(
                "Callback called for 'cancelled' task",
                address=address,
                t_name=task_name,
                c_name=coro_name,
                status=TaskStatusEnum.CANCELLED,
                timestamp=datetime.now(UTC),
            )
            return

        if task.exception():
            log.error(
                "Callback called for task with exception",
                address=address,
                t_name=task_name,
                c_name=coro_name,
                status=TaskStatusEnum.ERROR,
                exc=str(task.exception()),
            )

            return

        if task.done():
            log.info(
                "Callback called for successfully task",
                address=address,
                t_name=task_name,
                c_name=coro_name,
                status=TaskStatusEnum.SUCCESS,
                timestamp=datetime.now(UTC),
            )
