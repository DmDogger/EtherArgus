import asyncio
import os
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import TypeVar, final

import structlog

T = TypeVar("T")

log = structlog.getLogger(__name__)


@final
class ConcreteAsyncExecutor:
    def __init__(self) -> None:
        self._executor = ThreadPoolExecutor(max_workers=os.cpu_count())

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            log.error(
                "Occurred error in async executor",
                err_type=repr(exc_type),
                err=str(exc_val),
            )

        self._executor.shutdown(wait=True)

    async def __call__(self, fn: Callable[[], T]) -> T:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self._executor, fn)
