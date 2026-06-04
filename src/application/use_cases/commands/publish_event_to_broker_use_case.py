from collections.abc import Sequence

from application.interfaces.messaging.broker import EventPublisher
from domain.events.base import DomainEvent


class PublishEventToBrokerUseCase:
    def __init__(self, event_publisher: EventPublisher):
        self._event_publisher = event_publisher

    async def __call__(
        self,
        message: DomainEvent | Sequence[DomainEvent],
        topic: str | None = None,
        key: str | None = None,
    ) -> None:
        await self._event_publisher.publish(message=message, topic=topic, key=key)
