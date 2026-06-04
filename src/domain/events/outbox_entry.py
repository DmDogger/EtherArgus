from dataclasses import dataclass
from typing import final

from domain.events.base import DomainEvent


@final
@dataclass(slots=True)
class OutboxEntry(DomainEvent):
    event_type: str
    payload: DomainEvent
