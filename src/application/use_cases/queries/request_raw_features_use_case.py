import asyncio

import structlog

from application.dto.raw_etherscan_response_dto import RawEtherscanResponseDTO
from application.exceptions.exceptions import (
    BuildFeaturesError,
    InvalidEtherscanResponseStatus,
)
from application.interfaces.ether_fetcher import EtherFetcher

log = structlog.getLogger(__name__)


class RequestRawFeaturesUseCase:
    def __init__(self, fetcher: EtherFetcher):
        self._fetcher = fetcher

    async def __call__(self, address: str) -> RawEtherscanResponseDTO:
        try:
            response: RawEtherscanResponseDTO = await self._fetcher(address=address)

            return response
        except asyncio.TimeoutError as err:
            log.error("Occurred timeout error:", err=str(err), err_type=err.__name__)
            raise BuildFeaturesError(
                "Occurred error during building features."
                "Seems to be raised 'Timeout error' or API cannot to response at this moment"
                "Try to again a bit later."
            )

        except InvalidEtherscanResponseStatus as err:
            log.error(
                "Occurred invalid etherscan response status error:",
                err=str(err),
                err_type=err.__name__,
            )
        raise BuildFeaturesError(
            "Occurred error during building features. "
            "Seems to be etherscan cannot to return full information to analyze"
            "Try to choose another wallet to analysis"
        )
