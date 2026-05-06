from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class NormalTransactionDTO:
    to_address: str
    from_address: str
    is_error: int
    timestamp: int
    value: str


@dataclass(frozen=True, slots=True)
class InternalTransactionDTO:
    to_address: str
    from_address: str
    is_error: int
    timestamp: int
    value: str
    type: str


@dataclass(frozen=True, slots=True)
class TokenTransfersDTO:
    to_address: str
    from_address: str
    is_error: int
    timestamp: int
    value: Decimal
    contract_address: str
    token_name: str
    token_decimal: int
