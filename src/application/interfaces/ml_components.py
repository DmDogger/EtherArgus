"""Protocols for sklearn / XGBoost-style inference components."""

from typing import Protocol, Any

import numpy as np
from numpy.typing import ArrayLike

from domain.value_objects.risk_score_vo import RiskScoreValueObject


class MlScaler(Protocol):
    def __call__(self, data: Any): ...

    def transform(self, X: ArrayLike) -> np.ndarray: ...


class MlImputer(Protocol):
    def __call__(self, data: Any): ...

    def transform(self, X: ArrayLike) -> np.ndarray: ...


class MlClassificationModel(Protocol):
    def __call__(self, X: ArrayLike) -> RiskScoreValueObject: ...

    def predict(self, X: ArrayLike) -> np.ndarray: ...

    def predict_proba(self, X: ArrayLike) -> np.ndarray: ...
