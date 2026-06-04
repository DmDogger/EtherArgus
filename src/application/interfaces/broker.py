from typing import Protocol, Sequence

from domain.events.base import DomainEvent


class EventPublisher(Protocol):
    async def publish(
        self, message: DomainEvent, topic: str | None = None, key: str | None = None
    ) -> None: ...

    async def publish_many(
        self,
        messages: Sequence[DomainEvent],
        topic: str | None = None,
        key: str | None = None,
    ) -> None: ...
