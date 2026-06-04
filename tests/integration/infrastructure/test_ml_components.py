import pytest

from application.interfaces.features.feature_extraction import FeatureExtractionDirector
from domain.value_objects.risk_score_vo import RiskScoreValueObject
from infrastructure.ml.fraud_score_classifier import ConcreteFraudScoreClassifier


class TestMlFraudScoreClassifier:
    @pytest.mark.asyncio
    async def test_fraud_score_model_predict_and_returns_instance_of_risk_score_vo(
        self,
        fraud_score_classifier: ConcreteFraudScoreClassifier,
        director_of_feature_builder: FeatureExtractionDirector,
        ethereum_address: str,
        transactions,
        internal_transactions,
        token_transfers,
    ) -> None:

        features = director_of_feature_builder.build_features(
            ethereum_address,
            transactions,
            internal_transactions,
            token_transfers,
        )
        preds = fraud_score_classifier.predict(features)

        assert isinstance(preds, RiskScoreValueObject)
