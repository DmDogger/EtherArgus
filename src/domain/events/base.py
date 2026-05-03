from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import UUID, uuid4


@dataclass(slots=True, kw_only=True)
class DomainEvent(ABC):
    event_id: UUID = field(default_factory=lambda: uuid4())
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    aggregate_type: str | None = None
    aggregate_id: UUID | None = None
