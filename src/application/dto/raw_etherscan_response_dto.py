from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from application.dto.etherscan_transaction_dtos import NormalTransactionDTO

type RawEtherscanPayload = Mapping[str, str | list[dict[str, str]]]


@dataclass
class RawEtherscanResponseDTO:
    normal_transactions: RawEtherscanPayload | Sequence[NormalTransactionDTO]
    internal_transactions: RawEtherscanPayload
    token_transfers: RawEtherscanPayload
