import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, ParamSpec, TypeVar, final

import structlog

P = ParamSpec("P")
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

    async def __call__(self, fn: Callable[P, T], *args: P.args) -> T:
        loop = asyncio.get_running_loop()
        fut = loop.run_in_executor(self._executor, fn, *args)
        return await fut
