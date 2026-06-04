from typing import Mapping, TypeVar
from uuid import UUID

from sqlalchemy import select, not_, insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from domain.events.base import DomainEvent
from domain.events.outbox_entry import OutboxEntry
from infrastructure.db.mappers.outbox_db_mapper import OutboxDBMapper, OutboxTableValues
from infrastructure.db.tables.tables import outbox

T = TypeVar("T", bound=DomainEvent)


class SQLAlchemyCoreOutboxRepository:
    def __init__(self, connection: AsyncConnection, mapper: OutboxDBMapper):
        self._connection = connection
        self._mapper = mapper

    async def get_pending(self, limit: int = 10) -> list[OutboxEntry] | None:
        cursor_result_obj = await self._connection.execute(
            select(outbox).where(not_(outbox.c.is_processed.is_(True))).limit(limit)
        )

        raw_mappings_data = cursor_result_obj.mappings().all()

        if not raw_mappings_data:
            return None
        else:
            mapped_data = [self._mapper.to_event(value) for value in raw_mappings_data]
            return mapped_data

    async def save(self, event: T) -> list[OutboxEntry] | None:
        db_rows: Mapping[str, OutboxTableValues] = self._mapper.to_db_rows(event)

        cursor_result_obj = await self._connection.execute(
            insert(outbox).values(db_rows).returning(outbox)
        )

        raw_mappings_data = cursor_result_obj.mappings().all()

        if not raw_mappings_data:
            return None
        else:
            return [self._mapper.to_event(value) for value in raw_mappings_data]

    async def mark_processed(self, event_id: UUID) -> OutboxEntry | None:
        cursor_result_obj = await self._connection.execute(
            update(outbox)
            .where(outbox.c.event_id == event_id)  # type: ignore
            .values(is_processed=True)
            .returning(outbox)
        )

        raw_mappings_data = cursor_result_obj.mappings().first()

        if not raw_mappings_data:
            return None
        else:
            return self._mapper.to_event(raw_mappings_data)
