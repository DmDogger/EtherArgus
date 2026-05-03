from typing import Protocol

from application.interfaces.feature_extraction import BuiltFeatures
from domain.value_objects.risk_score_vo import RiskScoreValueObject


class FraudScoreClassifier(Protocol):
    def predict(self, data_to_predict: BuiltFeatures) -> RiskScoreValueObject: ...
