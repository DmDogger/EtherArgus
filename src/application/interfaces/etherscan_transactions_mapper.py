from typing import Protocol

from application.dto.etherscan_transaction_dtos import (
    InternalTransactionDTO,
    NormalTransactionDTO,
    TokenTransfersDTO,
)
from application.dto.raw_etherscan_response_dto import RawEtherscanResponseDTO


class EtherscanTransactionsMapper(Protocol):
    def from_raw_normal_transactions(
        self, raw: RawEtherscanResponseDTO
    ) -> list[NormalTransactionDTO]: ...

    def from_raw_internal_transactions(
        self, raw: RawEtherscanResponseDTO
    ) -> list[InternalTransactionDTO]: ...

    def from_raw_token_transfers(
        self, raw: RawEtherscanResponseDTO
    ) -> list[TokenTransfersDTO]: ...
