import pytest

from application.use_cases.commands.build_features_use_case import BuildFeaturesUseCase
from application.use_cases.commands.classify_fraud_use_case import ClassifyFraudUseCase
from domain.value_objects.risk_score_vo import RiskScoreValueObject


class TestClassifyFraudScoreUseCase:
    @pytest.mark.asyncio
    async def test_fraud_score_classifies_and_returns_risk_score_vo(
        self,
        ethereum_address: str,
        build_features_use_case: BuildFeaturesUseCase,
        classify_fraud_use_case: ClassifyFraudUseCase,
    ) -> None:
        features = await build_features_use_case(ethereum_address)

        fraud = await classify_fraud_use_case(built_features=features)

        assert isinstance(fraud, RiskScoreValueObject)
