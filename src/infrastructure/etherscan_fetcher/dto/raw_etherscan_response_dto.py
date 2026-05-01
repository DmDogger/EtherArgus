from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrastructure.etherscan_fetcher.fetcher.concrete_etherscan_fetcher import (
        RawEtherscanResponse,
    )


@dataclass
class RawEtherscanResponseDTO:
    normal_transactions: "RawEtherscanResponse"
    internal_transactions: "RawEtherscanResponse"
    token_transfers: "RawEtherscanResponse"
