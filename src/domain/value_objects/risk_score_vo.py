from dataclasses import dataclass
from typing import final

from domain.exceptions.exceptions import InvalidRiskScore


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class RiskScoreValueObject:
    value: float

    def __post_init__(self):
        if not (0.0 <= self.value <= 1.0):
            raise InvalidRiskScore(
                f"Risk score must be between 0 and 1, but got: {self.value}"
            )

    @classmethod
    def create(cls, *, score: float) -> "RiskScoreValueObject":
        return cls(value=score)
