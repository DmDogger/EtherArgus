from typing import Mapping, TypeVar
from uuid import UUID, uuid4
from datetime import datetime

from application.interfaces.messaging.serializer import Serializer
from domain.events.base import DomainEvent
from domain.events.outbox_entry import OutboxEntry

type OutboxTableValues = UUID | str | bool | datetime

T = TypeVar("T", bound=DomainEvent)


class OutboxDBMapper:
    def __init__(self, serializer: Serializer):
        self._serializer = serializer

    def to_event(self, rows: Mapping[str, OutboxTableValues]) -> OutboxEntry:
        return OutboxEntry(
            event_id=rows["event_id"],
            occurred_at=rows["occurred_at"],
            aggregate_type=rows["aggregate_type"],
            aggregate_id=rows["aggregate_id"],
            event_type=rows["event_type"],
            payload=self._serializer.loads(rows["payload"]),
        )

    def to_db_rows(self, event: T) -> Mapping[str, OutboxTableValues]:
        return {
            "event_id": event.event_id,
            "aggregate_type": event.aggregate_type or event.__class__.__name__,
            "aggregate_id": event.aggregate_id,
            "event_type": event.__class__.__name__,
            "payload": self._serializer.dumps(event),
            "occurred_at": event.occurred_at.replace(tzinfo=None),
        }
