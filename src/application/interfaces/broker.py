from typing import Protocol

from domain.events.base import DomainEvent


class EventPublisher(Protocol):
    async def publish(
        self, message: DomainEvent, topic: str | None = None, key: str | None = None
    ) -> None: ...
