from dataclasses import dataclass
from decimal import Decimal
from typing import final

from domain.enums import RiskLevelEnum
from domain.exceptions.exceptions import InvalidRiskLevel


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class RiskLevelValueObject:
    level: RiskLevelEnum

    def __post_init__(self):

        if not isinstance(self.level, RiskLevelEnum):
            raise InvalidRiskLevel(
                f"Risk level should be: low / medium / high, but got: {self.level}"
            )

    @classmethod
    def set(cls, *, risk: Decimal | float) -> "RiskLevelValueObject":
        if risk > 0.95:
            return cls(level=RiskLevelEnum.HIGH)
        elif risk > 0.5:
            return cls(level=RiskLevelEnum.MEDIUM)
        return cls(level=RiskLevelEnum.LOW)
