from dishka import FromDishka, Provider, Scope, provide
from faststream.kafka import KafkaBroker
from prometheus_client import Counter, Histogram

from application.interfaces.model_loader import ModelLoader
from application.interfaces.serializer import Serializer
from application.use_cases.commands.publish_event_to_broker_use_case import (
    PublishEventToBrokerUseCase,
)
from infrastructure.etherscan.building.etherscan_query_director import (
    EtherscanQueryDirector,
)
from infrastructure.etherscan.fetching.concrete_etherscan_fetcher import (
    ConcreteEtherscanFetcher,
)
from infrastructure.etherscan.fetching.etherscan_done_callback import (
    EtherscanDoneCallback,
)
from infrastructure.http.clients import AioHTTPClient, EtherscanHTTPClient
from config.broker import BrokerSettings

from infrastructure.broker.publisher import KafkaEventPublisher
from infrastructure.ml import ConcreteAsyncExecutor, ConcreteModelLoader
from infrastructure.serializer.json_serializer import JSONPickleSerializer


class InfrastructureProviders(Provider):
    scope = Scope.APP

    @provide(scope=Scope.APP)
    def broker_configuration(self) -> BrokerSettings:
        from config import broker as broker_pkg

        return broker_pkg.broker_settings

    @provide(scope=Scope.APP)
    def event_serializer(self) -> Serializer:
        return JSONPickleSerializer()

    @provide
    async def kafka_broker_network(
        self,
        broker_configuration: BrokerSettings,
    ) -> AsyncIterable[KafkaBroker]:
        broker = KafkaBroker(bootstrap_servers=broker_configuration.bootstrap_server)
        await broker.start()
        try:
            yield broker
        finally:
            await broker.stop()

    @provide(scope=Scope.APP)
    def kafka_event_publisher(
        self,
        broker: FromDishka[KafkaBroker],
        serializer: FromDishka[Serializer],
    ) -> KafkaEventPublisher:
        return KafkaEventPublisher(broker=broker, serializer=serializer)

    @provide
    def inference_metrics(self) -> tuple[Counter, Histogram]:
        err_counter = Counter(
            "ether_ml_fraud_analysis_requests_total", "Total analysis requests."
        )

        analysis_duration_seconds = Histogram(
            "ether_ml_fraud_analysis_duration_seconds",
            "Analysis pipeline duration in seconds.",
        )

        return err_counter, analysis_duration_seconds

    @provide
    async def aiohttp_client_session(self) -> AsyncIterable[ClientSession]:
        async with ClientSession() as session:
            yield session

    @provide
    async def model_loader(self) -> AsyncIterable[ModelLoader]:
        executor = ConcreteAsyncExecutor()
        try:
            yield ConcreteModelLoader(async_executor=executor)
        finally:
            executor.shutdown(wait=True)


class ApplicationProviders(Provider):
    scope = Scope.APP

    @provide
    def publish_event_to_broker_use_case(
        self,
        event_publisher: FromDishka[KafkaEventPublisher],
    ) -> PublishEventToBrokerUseCase:
        return PublishEventToBrokerUseCase(event_publisher=event_publisher)

    @provide
    def etherscan_fetcher(
        self,
        client: FromDishka[ClientSession],
    ) -> ConcreteEtherscanFetcher:
        return ConcreteEtherscanFetcher(
            EtherscanHTTPClient(AioHTTPClient(client)),
            EtherscanQueryDirector(),
            EtherscanDoneCallback(),
        )
