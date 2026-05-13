import asyncio
from asyncio import TaskGroup
from functools import partial
from typing import final

import structlog

from application.dto.raw_etherscan_response_dto import (
    RawEtherscanResponseDTO,
)
from application.exceptions.exceptions import InvalidEtherscanResponseStatus
from application.interfaces.done_callback import DoneCallback
from application.interfaces.ether_fetcher import EtherFetcher
from application.interfaces.http_client import EtherscanClient
from application.interfaces.metrics_client import MetricsClient
from application.interfaces.query_director import QueryDirector
from config.etherscan import etherscan_settings

log = structlog.getLogger(__name__)


@final
class ConcreteEtherscanFetcher:
    def __init__(
        self,
        client: EtherscanClient,
        director: QueryDirector,
        on_done_callback: DoneCallback,
    ):
        self._client = client
        self._director = director
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
            async with self._semaphore, TaskGroup() as group:
                tasks = [
                    group.create_task(
                        task, name=f"Task:{task.__name__}, Index: {index}"
                    )
                    for index, task in enumerate(
                        [
                            self._client(
                                params=self._director.build_transactions(
                                    address=address
                                )
                            ),
                            self._client(
                                params=self._director.build_internal_transactions(
                                    address=address
                                )
                            ),
                            self._client(
                                params=self._director.build_token_transfers(
                                    address=address
                                )
                            ),
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


@final
class MonitoredEtherscanFetcher:
    def __init__(self, fetcher: EtherFetcher, client: MetricsClient):
        self._fetcher = fetcher
        self._observability_client = client

    async def __call__(self, address: str) -> RawEtherscanResponseDTO:
        with self._observability_client:
            return await self._fetcher(address=address)
