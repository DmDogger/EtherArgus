from aiokafka import AIOKafkaConsumer

from application.use_cases.commands.publish_event_to_broker_use_case import (
    PublishEventToBrokerUseCase,
)
from domain.events.analysis_requested_event import AnalysisRequestedEvent
from domain.value_objects.correlation_id_vo import CorrelationId
from domain.value_objects.ethereum_address_vo import EthereumAddressValueObject


class TestPublishEventToBrokerUseCase:
    async def test_use_case_publish_single_event_success(
        self,
        ethereum_address: str,
        kafka_consumer: AIOKafkaConsumer,
        publish_event_to_broker_use_case: PublishEventToBrokerUseCase,
    ) -> None:

        await publish_event_to_broker_use_case(
            message=AnalysisRequestedEvent(
                correlation_id=CorrelationId.create(),
                requested_to=EthereumAddressValueObject.create(
                    address=ethereum_address,
                ),
            )
        )

        events = await kafka_consumer.getmany(timeout_ms=200)

        only_one_event = [event for event in events.values()]

        assert len(only_one_event) == 1

    async def test_use_case_publish_many_events_success(
        self,
        ethereum_address: str,
        kafka_consumer: AIOKafkaConsumer,
        publish_event_to_broker_use_case: PublishEventToBrokerUseCase,
    ) -> None:

        not_only_one = [
            AnalysisRequestedEvent(
                correlation_id=CorrelationId.create(),
                requested_to=EthereumAddressValueObject.create(
                    address=ethereum_address,
                ),
            )
            for _ in range(10)
        ]

        await publish_event_to_broker_use_case(not_only_one)

        events = await kafka_consumer.getmany(timeout_ms=200)

        all_events = [event for event in events.values()]

        assert len(*all_events) == 10
