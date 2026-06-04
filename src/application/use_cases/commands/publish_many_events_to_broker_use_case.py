from collections.abc import Sequence

from application.interfaces.messaging.broker import EventPublisher
from domain.events.base import DomainEvent


class PublishManyEventsToBrokerUseCase:
    def __init__(self, event_publisher: EventPublisher) -> None:
        self._event_publisher = event_publisher

    async def __call__(
        self,
        messages: Sequence[DomainEvent],
        topic: str | None = None,
        key: str | None = None,
    ) -> None:
        await self._event_publisher.publish_many(
            messages=messages, topic=topic, key=key
        )
