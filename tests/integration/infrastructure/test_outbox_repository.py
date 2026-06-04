from uuid import uuid4, UUID

import pytest

from domain.entities.analysis_result import AnalysisResult
from domain.events.address_analyzed import AddressAnalyzed
from domain.events.analysis_requested_event import AnalysisRequestedEvent
from domain.events.base import DomainEvent
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
        self,
        address_analyzed_event: AddressAnalyzed,
        transactional_seeded_outbox_repository: SQLAlchemyCoreOutboxRepository,
    ) -> None:

        returned_events = await transactional_seeded_outbox_repository.save(
            address_analyzed_event
        )

        assert all(
            event.aggregate_type == "AddressAnalyzed" for event in returned_events
        )

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
