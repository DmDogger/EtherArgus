import pytest

from domain.events.outbox_entry import OutboxEntry
from infrastructure.db.repositories.outbox_repository import (
    SQLAlchemyCoreOutboxRepository,
)


class TestSQLAlchemyCoreOutboxRepository:
    @pytest.mark.asyncio
    async def test_got_pending_events(
        self, transactional_seeded_outbox_repository: SQLAlchemyCoreOutboxRepository
    ) -> None:

        pending_events = await transactional_seeded_outbox_repository.get_pending(
            limit=5
        )

        assert all(isinstance(event, OutboxEntry) for event in pending_events)
