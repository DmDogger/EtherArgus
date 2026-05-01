from collections.abc import Mapping, Sequence
from typing import Any, TypeVar

from pydantic import BaseModel

from infrastructure.etherscan_fetcher.dto.raw_etherscan_response_dto import (
    RawEtherscanResponseDTO,
)
from infrastructure.etherscan_fetcher.schemas.etherscan_schemas import (
    NormalTransactionSchema,
    InternalTransactionSchema,
    TokenTransfersSchema,
)

T = TypeVar("T", bound=BaseModel)


class EtherscanMapper:
    def from_raw_normal_transactions(
        self, raw: RawEtherscanResponseDTO
    ) -> list[NormalTransactionSchema]:
        transactions_to_be_mapped = raw.normal_transactions["result"]
        return self._parse(NormalTransactionSchema, transactions_to_be_mapped)

    def from_raw_internal_transactions(
        self, raw: RawEtherscanResponseDTO
    ) -> list[InternalTransactionSchema]:
        transactions_to_be_mapped = raw.internal_transactions["result"]
        return self._parse(InternalTransactionSchema, transactions_to_be_mapped)

    def from_raw_token_transfers(
        self, raw: RawEtherscanResponseDTO
    ) -> list[TokenTransfersSchema]:
        transactions_to_be_mapped = raw.token_transfers["result"]
        return self._parse(TokenTransfersSchema, transactions_to_be_mapped)

    @staticmethod
    def _parse(
        schema: type[T],
        items: Sequence[Mapping[str, Any]],
    ) -> list[T]:
        return [schema.model_validate(item) for item in items]
