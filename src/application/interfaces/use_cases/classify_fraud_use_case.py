from typing import Protocol

from application.interfaces.features.feature_extraction import BuiltFeatures
from domain.value_objects.risk_score_vo import RiskScoreValueObject


class ClassifyFraudUseCase(Protocol):
    async def __call__(self, built_features: BuiltFeatures) -> RiskScoreValueObject: ...
