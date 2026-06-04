import asyncio
from typing import final, Sequence

from faststream.kafka import KafkaBroker

from application.exceptions.exceptions import InvalidPublishingMethodSelected
from application.interfaces.messaging.broker import EventPublisher
from application.interfaces.metrics.metrics_client import MetricsClient
from application.interfaces.messaging.serializer import Serializer
from config.broker import broker_settings
from domain.events.base import DomainEvent
from infrastructure.utils.utils import ensures_single_domain_event


@final
class KafkaEventPublisher:
    def __init__(self, broker: KafkaBroker, serializer: Serializer):
        self._broker = broker
        self._serializer = serializer

    async def publish(
        self,
        message: DomainEvent | Sequence[DomainEvent],
        topic: str | None = None,
        key: str | None = None,
    ) -> None:
        if not ensures_single_domain_event(message):
            await self._broker.publish(
                message=self._serializer.dumps(message),
                topic=broker_settings.topic or topic,
                key=key,
            )
        else:
            raise InvalidPublishingMethodSelected(
                f"You should use {self.__class__.__name__}'publish_many' method"
            )

    async def publish_many(
        self,
        messages: Sequence[DomainEvent],
        topic: str | None = None,
        key: str | None = None,
    ) -> None:

        coros_to_publish = [
            self._broker.publish(
                message=self._serializer.dumps(message), topic=topic, key=key
            )
            for message in messages
        ]

        await asyncio.gather(*coros_to_publish, return_exceptions=True)


@final
class MonitoredKafkaEventPublisher:
    def __init__(self, client: MetricsClient, event_publisher: EventPublisher):
        self._observability_client = client
        self._event_publisher = event_publisher

    async def publish(
        self,
        message: DomainEvent | list[DomainEvent],
        topic: str | None = None,
        key: str | None = None,
    ) -> None:
        with self._observability_client:
            await self._event_publisher.publish(message=message, topic=topic, key=key)
