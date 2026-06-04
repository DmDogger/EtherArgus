from typing import Callable, ParamSpec, Protocol, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


class AsyncExecutor(Protocol):
    async def __call__(self, fn: Callable[P, T], *args: P.args) -> T: ...
