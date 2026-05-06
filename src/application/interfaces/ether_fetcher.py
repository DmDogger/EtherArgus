from typing import Protocol

from application.dto.raw_etherscan_response_dto import (
    RawEtherscanPayload,
    RawEtherscanResponseDTO,
)


class EtherFetcher(Protocol):
    async def __call__(self, address: str) -> RawEtherscanResponseDTO: ...

    async def get_transactions(self, address: str) -> RawEtherscanPayload: ...

    async def get_internal_transactions(
        self,
        address: str,
    ) -> RawEtherscanPayload: ...

    async def get_token_transfers(self, address: str) -> RawEtherscanPayload: ...
