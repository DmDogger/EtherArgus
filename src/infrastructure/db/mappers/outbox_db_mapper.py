from typing import Mapping
from uuid import UUID
from datetime import datetime

from domain.events.outbox_entry import OutboxEntry

type OutboxTableValues = UUID | str | bool | datetime


class OutboxDBMapper:
    def to_event(self, rows: Mapping[str, OutboxTableValues]) -> OutboxEntry:
        return OutboxEntry(
            event_id=rows["event_id"],
            occurred_at=rows["occurred_at"],
            aggregate_type=rows["aggregate_type"],
            aggregate_id=rows["aggregate_id"],
            event_type=rows["event_type"],
            payload=rows["payload"],
        )

    def to_db_rows(self, event: OutboxEntry) -> Mapping[str, OutboxTableValues]:
        return {
            "event_id": event.event_id,
            "aggregate_type": event.aggregate_type,
            "aggregate_id": event.aggregate_id,
            "event_type": event.event_type,
            "payload": event.payload,
            "occurred_at": event.occurred_at.replace(tzinfo=None),
        }
