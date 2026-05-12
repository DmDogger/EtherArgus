from typing import final

from application.interfaces.fraud_score_classifier import FraudScoreClassifier
from application.interfaces.metrics_client import MetricsClient
from application.interfaces.ml_components import (
    MlClassificationModel,
    MlImputer,
    MlScaler,
)
from application.interfaces.feature_extraction import BuiltFeatures
from domain.value_objects.risk_score_vo import RiskScoreValueObject
from infrastructure.utils import from_raw_dict_to_dataframe


@final
class ConcreteFraudScoreClassifier:
    def __init__(
        self, model: MlClassificationModel, imputer: MlImputer, scaler: MlScaler
    ):
        self._model = model
        self._imputer = imputer
        self._scaler = scaler

    def predict(self, data_to_predict: BuiltFeatures, /) -> RiskScoreValueObject:
        features_as_dataframe = from_raw_dict_to_dataframe(data_to_predict)
        imputed = self._imputer(features_as_dataframe)
        scaled = self._scaler(imputed)
        ready_risk_score = self._model(scaled)
        return ready_risk_score


@final
class MonitoredFraudScoreClassifier:
    def __init__(self, predictor: FraudScoreClassifier, client: MetricsClient):
        self._predictor = predictor
        self._observability_client = client

    def predict(self, data_to_predict: BuiltFeatures, /) -> RiskScoreValueObject:
        with self._observability_client:
            return self._predictor.predict(data_to_predict)
