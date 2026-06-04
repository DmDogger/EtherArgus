from typing import Protocol

from application.dto.etherscan_transaction_dtos import (
    TokenTransfersDTO,
    NormalTransactionDTO,
    InternalTransactionDTO,
)
from application.dto.raw_etherscan_response_dto import RawEtherscanResponseDTO

type TransactionsSequence = tuple[
    list[NormalTransactionDTO], list[InternalTransactionDTO], list[TokenTransfersDTO]
]


class RawResponseMapper(Protocol):
    def map_all(
        self, raw_response: RawEtherscanResponseDTO
    ) -> TransactionsSequence: ...
