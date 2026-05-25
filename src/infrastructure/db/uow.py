import contextvars
from typing import Self, ClassVar

import structlog
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncTransaction

log = structlog.getLogger(__name__)


class ConcreteUnitOfWork:
    _transaction: ClassVar[contextvars.ContextVar[AsyncTransaction]] = (
        contextvars.ContextVar("_transaction")
    )

    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def __aenter__(self) -> Self:
        tr = await self._connection.begin()
        self._transaction.set(tr)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        tr = self._transaction.get()

        if exc_type:
            log.error(
                "Occurred error during database transaction",
                exc=str(exc_val),
                exc_type=exc_type,
            )
            await tr.rollback()
        else:
            await tr.commit()

        await self._connection.close()
