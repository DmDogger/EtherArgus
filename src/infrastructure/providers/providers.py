from collections.abc import AsyncIterable
from dataclasses import dataclass

from aiohttp import ClientSession
from dishka import FromDishka, Provider, Scope, provide
from prometheus_client import Counter, Histogram

from application.interfaces.model_loader import ModelLoader
from infrastructure.etherscan_fetcher.fetcher.concrete_etherscan_fetcher import (
    ConcreteEtherscanFetcher,
)
from infrastructure.etherscan_fetcher.fetcher.etherscan_done_callback import (
    EtherscanDoneCallback,
)
from infrastructure.http.clients import AioHTTPClient, EtherscanHTTPClient
from infrastructure.ml import ConcreteAsyncExecutor, ConcreteModelLoader


class InfrastructureProviders(Provider):
    scope = Scope.APP

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
    def etherscan_fetcher(
        self,
        client: FromDishka[ClientSession],
    ) -> ConcreteEtherscanFetcher:
        return ConcreteEtherscanFetcher(
            EtherscanHTTPClient(AioHTTPClient(client)),
            EtherscanDoneCallback(),
        )
