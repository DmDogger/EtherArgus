from abc import ABC
from copy import copy
from dataclasses import dataclass, field
from typing import TypeVar, Any
from uuid import UUID, uuid4

from domain.events.base import DomainEvent

T = TypeVar("T", bound=DomainEvent)


@dataclass(slots=True, kw_only=True)
class AbstractAggregateRoot(ABC):
    id: UUID = field(default_factory=lambda: uuid4())
    _events: list[DomainEvent] = field(default_factory=list, repr=False, kw_only=True)

    @property
    def aggregate_type(self):
        return self.__class__.__name__

    def _register_event(self, event_class: type[T], **kwargs: Any) -> None:
        event = event_class(
            aggregate_type=self.aggregate_type, aggregate_id=self.id, **kwargs
        )
        self._events.append(event)

    def pop_events(self) -> list[DomainEvent]:
        events = copy(self._events)
        self._events.clear()
        return events
