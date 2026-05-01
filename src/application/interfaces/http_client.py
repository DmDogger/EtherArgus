from typing import Protocol, Mapping, Any

type RequestParams = Mapping[str, Any]
type HTTPResponse = Mapping[str, Any]


class HTTPClient(Protocol):
    async def get(
        self, params: RequestParams, url: str | None = None
    ) -> HTTPResponse: ...


class EtherscanClient(Protocol):
    async def __call__(self, params: RequestParams, url: str | None = None): ...
