from collections.abc import Callable

import pytest

from domain.entities.analysis_result import AnalysisResult
from domain.events.base import DomainEvent
from domain.value_objects.risk_score_vo import RiskScoreValueObject


@pytest.fixture
def create_analysis_result() -> Callable[[type[DomainEvent]], AnalysisResult]:
    def _analysis_result_factory(event_class: type[DomainEvent]) -> AnalysisResult:
        analysis_result = AnalysisResult.create(
            event_class=event_class,
            address="0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97",
            score=RiskScoreValueObject.create(score=0.5),
        )
        return analysis_result

    return _analysis_result_factory
