from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing_extensions import Literal


class _ConfigurationMixin(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True, extra="ignore", strict=False, frozen=True
    )


class _BaseFieldsMixin(BaseModel):
    to_address: str = Field(
        ..., alias="to", examples=["0xc5102fe9359fd9a28f877a67e36b0f050d81a3cc"]
    )
    from_address: str = Field(
        ..., alias="from", examples=["0x2449ecef5012f0a0e153b278ef4fcc9625bc4c78"]
    )
    is_error: int = Field(..., alias="isError", examples=["1", "0"])
    timestamp: int = Field(..., alias="timeStamp")

    @field_validator("to_address", "from_address", mode="before")
    @classmethod
    def _normalize_hex_address(cls, value: object) -> str:
        if not isinstance(value, str):
            return str(value)
        return value.lower()


class NormalTransactionSchema(_BaseFieldsMixin, _ConfigurationMixin):
    value: str = Field(..., alias="value", examples=["0", "583713"])


class InternalTransactionSchema(_BaseFieldsMixin, _ConfigurationMixin):
    value: str = Field(..., examples=["0", "583713"])
    type: Literal[
        "create",
        "call",
        "suicide",
        "self-destruct",
        "reward",
        "delegatecall",
        "staticcall",
        "callcode",
    ] = Field(...)


class TokenTransfersSchema(_BaseFieldsMixin, _ConfigurationMixin):
    value: Decimal = Field(..., examples=["0", "583713"])
    contract_address: str = Field(..., alias="contractAddress")
    token_name: str = Field(..., alias="tokenName")
    token_decimal: int = Field(..., alias="tokenDecimal")
    is_error: int = Field(default=0, alias="isError")

    @field_validator("contract_address", mode="before")
    @classmethod
    def _normalize_contract_address(cls, value: object) -> str:
        if not isinstance(value, str):
            return str(value)
        return value.lower()
