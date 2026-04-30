from collections.abc import AsyncIterable

from aiohttp import ClientSession
from dishka import FromDishka, Provider, Scope, provide

from infrastructure.etherscan_fetcher.concrete_etherscan_fetcher import (
    ConcreteEtherscanFetcher,
)


class InfrastructureProviders(Provider):
    scope = Scope.APP

    @provide
    async def aiohttp_client_session(self) -> AsyncIterable[ClientSession]:
        async with ClientSession() as session:
            yield session


class ApplicationProviders(Provider):
    scope = Scope.APP

    @provide
    def etherscan_fetcher(
        self,
        client: FromDishka[ClientSession],
    ) -> ConcreteEtherscanFetcher:
        return ConcreteEtherscanFetcher(client)
