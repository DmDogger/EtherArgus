from uuid import uuid4, UUID

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

    @pytest.mark.asyncio
    async def test_repository_saves_and_returns_result(
        self, transactional_seeded_outbox_repository: SQLAlchemyCoreOutboxRepository
    ) -> None:
        event_to_save = OutboxEntry(
            aggregate_type="test_type",
            aggregate_id=uuid4(),
            event_type="test_type",
            payload="test_payload",
        )

        returned_event = await transactional_seeded_outbox_repository.save(
            event_to_save
        )

        assert all(event.payload == "test_payload" for event in returned_event)

    @pytest.mark.asyncio
    async def test_repository_mark_as_processed_with_success(
        self,
        transactional_seeded_outbox_repository: SQLAlchemyCoreOutboxRepository,
        static_uuid: UUID,
    ) -> None:
        await transactional_seeded_outbox_repository.mark_processed(
            event_id=static_uuid
        )

        # we mark as processed, so there are no more values in 'pending' status.
        here_will_be_none = await transactional_seeded_outbox_repository.get_pending()

        assert here_will_be_none is None
