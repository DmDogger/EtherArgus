from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest
import pytest_asyncio

from application.interfaces.use_cases.build_features import BuildFeaturesUseCase
from application.interfaces.features.feature_extraction import FeatureExtractionDirector
from application.interfaces.etherscan.etherscan_transactions_mapper import (
    EtherscanTransactionsMapper,
)
from application.interfaces.ml.fraud_score_classifier import FraudScoreClassifier
from application.interfaces.etherscan.response_mapper import RawResponseMapper
from application.use_cases.commands.build_features_use_case import (
    BuildFeaturesUseCase as ConcreteBuildFeaturesUseCase,
)
from application.use_cases.commands.classify_fraud_use_case import ClassifyFraudUseCase
from application.use_cases.commands.publish_event_to_broker_use_case import (
    PublishEventToBrokerUseCase,
)
from application.use_cases.queries.request_raw_features_use_case import (
    RequestRawFeaturesUseCase,
)
from infrastructure.ml.concrete_async_executor import ConcreteAsyncExecutor
from infrastructure.raw_response_mapper.mapper import ConcreteRawResponseMapper


@pytest_asyncio.fixture
async def request_features_use_case(etherscan_fetcher) -> RequestRawFeaturesUseCase:
    return RequestRawFeaturesUseCase(fetcher=etherscan_fetcher)


@pytest_asyncio.fixture
async def build_features_use_case(
    director_of_feature_builder: FeatureExtractionDirector,
    request_features_use_case: RequestRawFeaturesUseCase,
    etherscan_mapper: EtherscanTransactionsMapper,
) -> BuildFeaturesUseCase:
    response_mapper: RawResponseMapper = ConcreteRawResponseMapper(
        mapper=etherscan_mapper,
    )
    return ConcreteBuildFeaturesUseCase(
        director=director_of_feature_builder,
        response_mapper=response_mapper,
        request_raw_features_use_case=request_features_use_case,
    )


@pytest_asyncio.fixture
async def classify_fraud_use_case(
    fraud_score_classifier: FraudScoreClassifier,
) -> ClassifyFraudUseCase:
    return ClassifyFraudUseCase(
        async_executor=ConcreteAsyncExecutor(),
        fraud_score_classifier=fraud_score_classifier,
    )


@pytest.fixture
def kafka_bootstrap_servers() -> Generator[str, None, None]:
    import asyncio

    from aiokafka.admin import AIOKafkaAdminClient, NewTopic
    from aiokafka.errors import TopicAlreadyExistsError
    from config.broker import broker_settings
    from testcontainers.kafka import RedpandaContainer

    container = RedpandaContainer()
    container.start(timeout=120)
    bootstrap = container.get_bootstrap_server()

    async def _create_topic() -> None:
        admin = AIOKafkaAdminClient(bootstrap_servers=bootstrap)
        await admin.start()
        try:
            resp = await admin.create_topics(
                [
                    NewTopic(
                        name=broker_settings.topic,
                        num_partitions=1,
                        replication_factor=1,
                    ),
                ],
                timeout_ms=15_000,
            )
            for row in resp.to_object().get("topic_errors", []):
                if row["error_code"] not in (0, TopicAlreadyExistsError.errno):
                    raise RuntimeError(f"create_topics failed: {row}")
        finally:
            await admin.close()

    asyncio.run(_create_topic())
    try:
        yield bootstrap
    finally:
        container.stop()


@pytest_asyncio.fixture
async def kafka_consumer(kafka_bootstrap_servers: str) -> AsyncGenerator[Any, None]:
    import uuid

    from aiokafka import AIOKafkaConsumer
    from config.broker import broker_settings

    consumer = AIOKafkaConsumer(
        bootstrap_servers=kafka_bootstrap_servers,
        group_id=f"ether_ml_fraud_pytest_{uuid.uuid4().hex}",
        auto_offset_reset="earliest",
        enable_auto_commit=False,
    )
    await consumer.start()
    try:
        consumer.subscribe([broker_settings.topic])
        yield consumer
    finally:
        await consumer.stop()


@pytest_asyncio.fixture
async def kafka_broker_integration(
    kafka_bootstrap_servers: str,
) -> AsyncGenerator[Any, None]:
    from faststream.kafka import KafkaBroker

    broker = KafkaBroker(bootstrap_servers=kafka_bootstrap_servers)
    await broker.start()
    try:
        yield broker
    finally:
        await broker.stop()


@pytest_asyncio.fixture
async def kafka_publish_adapter(
    kafka_broker_integration,
):
    from infrastructure.broker.publisher import KafkaEventPublisher
    from infrastructure.serializer.json_serializer import JSONPickleSerializer

    return KafkaEventPublisher(
        broker=kafka_broker_integration,
        serializer=JSONPickleSerializer(),
    )


@pytest_asyncio.fixture
async def publish_event_to_broker_use_case(
    kafka_publish_adapter,
) -> PublishEventToBrokerUseCase:
    return PublishEventToBrokerUseCase(event_publisher=kafka_publish_adapter)
