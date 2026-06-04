from sqlalchemy import select, not_
from sqlalchemy.ext.asyncio import AsyncConnection

from domain.events.outbox_entry import OutboxEntry
from infrastructure.db.mappers.outbox_db_mapper import OutboxDBMapper
from infrastructure.db.tables.tables import outbox

class SQLAlchemyCoreOutboxRepository:
    def __init__(self, connection: AsyncConnection, mapper: OutboxDBMapper):
        self._connection = connection
        self._mapper = mapper

    async def get_pending(self, limit: int = 10) -> list[OutboxEntry] | None:

        cursor_result_obj = await self._connection.execute(
            select(outbox).where(not_(outbox.c.is_processed.is_(True))).limit(limit)
        )

        raw_mappings_data = cursor_result_obj.mappings().all()

        if raw_mappings_data:
            mapped_data = [self._mapper.to_event(value) for value in raw_mappings_data]
            return mapped_data
        else:
            return None
