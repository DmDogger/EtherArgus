from typing import Protocol


class UnitOfWork(Protocol):
    async def __aenter__(self): ...

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
