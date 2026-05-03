import pytest

from domain.value_objects.risk_score_vo import RiskScoreValueObject
from infrastructure.feature_extractor.director_of_feature_extraction import (
    DirectorOfFeatureExtraction,
)
from infrastructure.ml.fraud_score_classifier import ConcreteFraudScoreClassifier


class TestMlFraudScoreClassifier:
    @pytest.mark.asyncio
    async def test_fraud_score_model_predict_and_returns_instance_of_risk_score_vo(
        self,
        fraud_score_classifier: ConcreteFraudScoreClassifier,
        director_of_feature_builder: DirectorOfFeatureExtraction,
    ) -> None:

        features = director_of_feature_builder()
        preds = fraud_score_classifier.predict(features)

        assert isinstance(preds, RiskScoreValueObject)