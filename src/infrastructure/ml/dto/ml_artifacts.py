from dataclasses import dataclass
from typing import Sequence

from application.interfaces.ml_components import (
    MlClassificationModel,
    MlImputer,
    MlScaler,
)


@dataclass
class MLArtifacts:
    model: MlClassificationModel
    imputer: MlImputer
    scaler: MlScaler
    feature_order: Sequence[str]
