from typing import Mapping, Protocol, Sequence

type RawEtherscanPayload = Mapping[str, str | list[dict[str, str]]]


class EtherscanHTTPClient(Protocol):
    async def __call__(self, address: str) -> Sequence[RawEtherscanPayload]: ...

    async def get_transactions(self, address: str) -> RawEtherscanPayload: ...

    async def get_internal_transactions(
        self,
        address: str,
    ) -> RawEtherscanPayload: ...

    async def get_token_transfers(self, address: str) -> RawEtherscanPayload: ...
