from asyncio import Task
from datetime import datetime, UTC
from typing import final

import structlog

from infrastructure.etherscan_fetcher.enums import TaskStatusEnum

log = structlog.getLogger(__name__)


@final
class EtherscanDoneCallback:
    def __call__(self, task: Task, address: str) -> None:
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
                "Callback called for successful task",
                address=address,
                t_name=task_name,
                c_name=coro_name,
                status=TaskStatusEnum.SUCCESS,
                timestamp=datetime.now(UTC),
            )
            return
