from datetime import datetime, UTC
from dataclasses import dataclass, field
from typing import final, TypeVar, Literal

from domain.entities.base import AbstractAggregateRoot
from domain.events.base import DomainEvent
from domain.value_objects.correlation_id_vo import CorrelationId
from domain.value_objects.ethereum_address_vo import EthereumAddressValueObject
from domain.value_objects.risk_level import RiskLevelValueObject
from domain.value_objects.risk_score_vo import RiskScoreValueObject

T = TypeVar("T", bound=DomainEvent)


@final
@dataclass(slots=True, kw_only=True)
class AnalysisResult(AbstractAggregateRoot):
    address: EthereumAddressValueObject
    score: RiskScoreValueObject
    level: RiskLevelValueObject
    processed_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        event_class: type[T],
        address: str,
        score: float,
        level: Literal["low", "medium", "high"],
    ) -> "AnalysisResult":
        analysis_result = cls(
            address=EthereumAddressValueObject.create(address=address),
            score=RiskScoreValueObject.create(score=score),
            level=RiskLevelValueObject.set(level=level),
            processed_at=datetime.now(UTC),
        )
        analysis_result._register_event(
            event_class=event_class,
            requested_to=analysis_result.address,
            correlation_id=CorrelationId,
        )
        return analysis_result
