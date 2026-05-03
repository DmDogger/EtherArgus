from dataclasses import dataclass
from typing import final, Literal

from domain.exceptions.exceptions import InvalidRiskLevel


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class RiskLevelValueObject:
    level: Literal["low", "medium", "high"]

    def __post_init__(self):
        if self.level not in ("low", "medium", "high"):
            raise InvalidRiskLevel(
                f"Risk level should be: low / medium / high, but got: {self.level}"
            )

    @classmethod
    def set(cls, *, level: Literal["low", "medium", "high"]) -> "RiskLevelValueObject":
        return cls(level=level)
