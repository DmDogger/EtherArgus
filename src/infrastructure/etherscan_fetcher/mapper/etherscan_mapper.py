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
        result_records = raw.normal_transactions["result"]
        return self._parse(NormalTransactionSchema, result_records)

    def from_raw_internal_transactions(
        self, raw: RawEtherscanResponseDTO
    ) -> list[InternalTransactionSchema]:
        result_records = raw.internal_transactions["result"]
        return self._parse(InternalTransactionSchema, result_records)

    def from_raw_token_transfers(
        self, raw: RawEtherscanResponseDTO
    ) -> list[TokenTransfersSchema]:
        result_records = raw.token_transfers["result"]
        return self._parse(TokenTransfersSchema, result_records)

    @staticmethod
    def _parse(
        schema: type[T],
        items: Sequence[Mapping[str, Any]],
    ) -> list[T]:
        return [schema.model_validate(item) for item in items]
