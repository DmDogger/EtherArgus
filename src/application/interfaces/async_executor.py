from typing import Any, Callable, Protocol


class AsyncExecutor(Protocol):
    async def __call__(self, fn: Callable[[], Any]) -> Any: ...
