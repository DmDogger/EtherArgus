from application.interfaces.ml.async_executor import AsyncExecutor
from application.interfaces.features.feature_extraction import BuiltFeatures
from application.interfaces.ml.fraud_score_classifier import FraudScoreClassifier
from domain.value_objects.risk_score_vo import RiskScoreValueObject


class ClassifyFraudUseCase:
    def __init__(
        self,
        async_executor: AsyncExecutor,
        fraud_score_classifier: FraudScoreClassifier,
    ):
        self._async_executor = async_executor
        self._fraud_score_classifier = fraud_score_classifier

    async def __call__(self, built_features: BuiltFeatures) -> RiskScoreValueObject:
        risk_score: RiskScoreValueObject = await self._async_executor(
            self._fraud_score_classifier.predict, built_features
        )
        return risk_score
