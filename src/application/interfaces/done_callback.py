from asyncio import Protocol, Task


class DoneCallback(Protocol):
    def __call__(self, task: Task, address: str) -> None: ...
