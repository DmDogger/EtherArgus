import json
from typing import Any

import joblib

from config.model_registry import model_registry_settings


class ModelRegistry:
    @staticmethod
    def load_scaler_from_disk() -> object:
        return joblib.load(model_registry_settings.scaler_path)

    @staticmethod
    def load_imputer_from_disk() -> object:
        return joblib.load(model_registry_settings.imputer_path)

    @staticmethod
    def load_model_from_disk() -> object:
        return joblib.load(model_registry_settings.model_path)

    @staticmethod
    def load_feature_order_from_disk() -> Any:
        raw = model_registry_settings.feature_order_path.read_text(encoding="utf-8")
        return json.loads(raw)
