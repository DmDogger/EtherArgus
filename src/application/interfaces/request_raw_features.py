from typing import Protocol

from application.dto.raw_etherscan_response_dto import RawEtherscanResponseDTO


class RequestRawFeaturesUseCase(Protocol):
    async def __call__(self, address: str) -> RawEtherscanResponseDTO: ...
