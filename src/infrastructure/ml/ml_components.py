from typing import Any, final

from numpy import ndarray, dtype

from domain.value_objects.risk_score_vo import RiskScoreValueObject
from infrastructure.ml.dto.ml_artifacts import MLArtifacts

type ArrayLikeOutput = ndarray[tuple[Any, ...], dtype[Any]]


@final
class ConcreteMlScaler:
    """Applies the loaded scaler transform to feature matrices."""

    def __init__(self, ml_artifacts: MLArtifacts):
        self._artifacts = ml_artifacts

    def __call__(self, data: Any) -> ArrayLikeOutput:
        return self._artifacts.scaler.transform(data)


@final
class ConcreteMlInputer:
    """Applies the loaded imputer transform to feature matrices."""

    def __init__(self, ml_artifacts: MLArtifacts):
        self._artifacts = ml_artifacts

    def __call__(self, data: Any) -> ArrayLikeOutput:
        return self._artifacts.imputer.transform(data)


@final
class ConcreteMlClassificationModel:
    """Runs the fraud classifier pipeline: impute -> scale -> ``predict_proba`` -> risk score."""

    def __init__(self, ml_artifacts: MLArtifacts):
        self._artifacts = ml_artifacts

    def __call__(self, data: Any) -> RiskScoreValueObject:
        y_probs = self._artifacts.model.predict_proba(data)
        return RiskScoreValueObject(score=y_probs[0][1])
