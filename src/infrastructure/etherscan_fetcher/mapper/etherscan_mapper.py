from collections.abc import Mapping, Sequence
from typing import Any, TypeVar, cast

from pydantic import BaseModel

from application.dto.etherscan_transaction_dtos import (
    InternalTransactionDTO,
    NormalTransactionDTO,
    TokenTransfersDTO,
)
from application.dto.raw_etherscan_response_dto import (
    RawEtherscanPayload,
    RawEtherscanResponseDTO,
)
from infrastructure.etherscan_fetcher.schemas.etherscan_schemas import (
    InternalTransactionSchema,
    NormalTransactionSchema,
    TokenTransfersSchema,
)

T = TypeVar("T", bound=BaseModel)


class _FromExternalToDTO:
    @staticmethod
    def normal_transaction_schema_to_dto(
        model: NormalTransactionSchema,
    ) -> NormalTransactionDTO:
        return NormalTransactionDTO(
            to_address=model.to_address,
            from_address=model.from_address,
            is_error=model.is_error,
            timestamp=model.timestamp,
            value=model.value,
        )

    @staticmethod
    def internal_transaction_schema_to_dto(
        model: InternalTransactionSchema,
    ) -> InternalTransactionDTO:
        return InternalTransactionDTO(
            to_address=model.to_address,
            from_address=model.from_address,
            is_error=model.is_error,
            timestamp=model.timestamp,
            value=model.value,
            type=model.type,
        )

    @staticmethod
    def token_transfers_schema_to_dto(model: TokenTransfersSchema) -> TokenTransfersDTO:
        return TokenTransfersDTO(
            to_address=model.to_address,
            from_address=model.from_address,
            is_error=model.is_error,
            timestamp=model.timestamp,
            value=model.value,
            contract_address=model.contract_address,
            token_name=model.token_name,
            token_decimal=model.token_decimal,
        )


class EtherscanMapper:

    def from_raw_normal_transactions(
        self, raw: RawEtherscanResponseDTO
    ) -> list[NormalTransactionDTO]:
        result_records = cast(RawEtherscanPayload, raw.normal_transactions)["result"]
        parsed = self._parse(NormalTransactionSchema, result_records)
        return [_FromExternalToDTO.normal_transaction_schema_to_dto(m) for m in parsed]

    def from_raw_internal_transactions(
        self, raw: RawEtherscanResponseDTO
    ) -> list[InternalTransactionDTO]:
        result_records = raw.internal_transactions["result"]
        parsed = self._parse(InternalTransactionSchema, result_records)
        return [
            _FromExternalToDTO.internal_transaction_schema_to_dto(m) for m in parsed
        ]

    def from_raw_token_transfers(
        self, raw: RawEtherscanResponseDTO
    ) -> list[TokenTransfersDTO]:
        result_records = raw.token_transfers["result"]
        parsed = self._parse(TokenTransfersSchema, result_records)
        return [_FromExternalToDTO.token_transfers_schema_to_dto(m) for m in parsed]

    @staticmethod
    def _parse(
        schema: type[T],
        items: Sequence[Mapping[str, Any]],
    ) -> list[T]:
        return [schema.model_validate(item) for item in items]
